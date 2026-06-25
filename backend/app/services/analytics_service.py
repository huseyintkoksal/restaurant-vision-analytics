"""Analytics service — owns the engine, the demo loop, and realtime fan-out.

This is the runtime hub. It builds an :class:`AnalyticsEngine` from the
configured zones, drives it (in demo mode via a synthetic detector), broadcasts
each aggregate snapshot to WebSocket subscribers, and periodically persists
snapshots, evaluates alerts, and prunes old data.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging

from sqlmodel import Session

from app.config import Settings, get_settings
from app.database.init_db import DEMO_CAMERA_ID, default_demo_zones
from app.database.repositories import AlertRepository, SnapshotRepository, ZoneRepository
from app.database.session import get_engine
from app.models.analytics_snapshot import AnalyticsSnapshot
from app.services.alert_service import AlertEvaluator
from app.services.retention_service import RetentionService
from app.vision.analytics_engine import AnalyticsEngine
from app.vision.mock_detector import SyntheticDetector

logger = logging.getLogger("rva.analytics")


class ConnectionManager:
    """Tracks active WebSocket subscribers and fans out JSON messages."""

    def __init__(self) -> None:
        self._connections: set = set()

    async def connect(self, websocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)

    def disconnect(self, websocket) -> None:
        self._connections.discard(websocket)

    @property
    def count(self) -> int:
        return len(self._connections)

    async def broadcast(self, message: dict) -> None:
        stale = []
        for ws in list(self._connections):
            try:
                await ws.send_json(message)
            except Exception:  # connection dropped
                stale.append(ws)
        for ws in stale:
            self.disconnect(ws)


class AnalyticsService:
    """Runtime hub for analytics, demo loop, and realtime broadcasting."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.connections = ConnectionManager()
        self.engine: AnalyticsEngine | None = None
        self.alerts = AlertEvaluator(
            queue_threshold=0.8, occupancy_threshold=22
        )
        self.retention = RetentionService(self.settings.data_retention_days)
        self._task: asyncio.Task | None = None
        self._persist_every = 5  # persist a snapshot roughly every 5 ticks
        self._prune_every = 600

    # -- engine wiring ----------------------------------------------------
    def _load_runtime_zones(self):
        with Session(get_engine()) as session:
            records = ZoneRepository(session).list()
        if not records:
            records = default_demo_zones()
        return [r.to_runtime() for r in records]

    def configure(self) -> AnalyticsEngine:
        """Build the analytics engine from configured zones."""
        detector = SyntheticDetector(
            seed=self.settings.demo_seed,
            step_seconds=self.settings.live_update_interval_seconds,
            base_arrival_rate=self.settings.demo_arrival_rate,
        )
        self.engine = AnalyticsEngine(
            detector=detector,
            zones=self._load_runtime_zones(),
            camera_id=DEMO_CAMERA_ID,
            track_ttl_seconds=self.settings.track_ttl_seconds,
            raw_frame_storage=self.settings.enable_raw_frame_storage,
        )
        return self.engine

    def get_engine(self) -> AnalyticsEngine:
        if self.engine is None:
            self.configure()
        assert self.engine is not None
        return self.engine

    # -- demo loop --------------------------------------------------------
    async def start_demo_loop(self) -> None:
        if not self.settings.enable_demo_mode:
            logger.info("Demo mode disabled; analytics loop not started.")
            return
        if self._task is not None:
            return
        self.get_engine()
        self._task = asyncio.create_task(self._run(), name="rva-demo-loop")
        logger.info("Demo analytics loop started.")

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _run(self) -> None:
        interval = max(0.2, self.settings.live_update_interval_seconds)
        tick = 0
        while True:
            try:
                snapshot = self.get_engine().tick()
                await self.connections.broadcast(snapshot)
                tick += 1
                if tick % self._persist_every == 0:
                    self._persist_and_alert(snapshot)
                if tick % self._prune_every == 0:
                    self._prune()
            except asyncio.CancelledError:
                raise
            except Exception:  # never let the loop die on a transient error
                logger.exception("Analytics loop iteration failed")
            await asyncio.sleep(interval)

    # -- persistence & alerts --------------------------------------------
    def tick_once(self, persist: bool = False) -> dict:
        """Run a single engine tick (used by tests and manual triggers)."""
        snapshot = self.get_engine().tick()
        if persist:
            self._persist_and_alert(snapshot)
        return snapshot

    def _persist_and_alert(self, snapshot: dict) -> None:
        with Session(get_engine()) as session:
            SnapshotRepository(session).add(
                AnalyticsSnapshot(
                    camera_id=snapshot["camera_id"],
                    total_occupancy=snapshot["occupancy"]["total"],
                    queue_count=snapshot["queue"]["count"],
                    queue_pressure=snapshot["queue"]["pressure_score"],
                    payload={
                        "occupancy": snapshot["occupancy"],
                        "queue": snapshot["queue"],
                        "tables_summary": self.get_engine().table_tracker.summary(0),
                    },
                )
            )
            alert_repo = AlertRepository(session)
            for alert in self.alerts.evaluate(snapshot):
                alert_repo.add(alert)

    def _prune(self) -> None:
        with Session(get_engine()) as session:
            result = self.retention.prune(session)
        logger.info("Retention prune: %s", result)


_service: AnalyticsService | None = None


def get_analytics_service() -> AnalyticsService:
    """Return the process-wide analytics service singleton."""
    global _service
    if _service is None:
        _service = AnalyticsService()
    return _service


def reset_analytics_service() -> None:
    """Reset the singleton (test helper)."""
    global _service
    _service = None
