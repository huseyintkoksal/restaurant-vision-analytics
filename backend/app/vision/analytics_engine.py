"""Analytics engine — orchestrates the privacy-first vision pipeline.

The engine wires a :class:`~app.vision.detector_base.Detector` to the analytics
modules and produces **aggregate, anonymous** snapshots. It is detector-agnostic:
demo mode injects a :class:`SyntheticDetector`, while real deployments can inject
an OpenCV/YOLO adapter without changing any analytics code.

Privacy boundary: only anonymous foot points and box centroids cross from the
detector into this engine. No imagery, identity, or personal attribute is stored.
"""

from __future__ import annotations

import time
from collections import deque

from app.utils.time import iso, utcnow
from app.vision.detector_base import Detector
from app.vision.heatmap import HeatmapGrid
from app.vision.occupancy import OccupancyAccumulator, compute_occupancy
from app.vision.queue import compute_queue_metrics
from app.vision.table_usage import TableUsageTracker
from app.vision.tracker import CentroidTracker
from app.vision.zones import Zone


class AnalyticsEngine:
    """Runs detection + analytics and exposes aggregate snapshots."""

    def __init__(
        self,
        detector: Detector,
        zones: list[Zone],
        camera_id: str = "demo-camera-1",
        track_ttl_seconds: float = 5.0,
        queue_threshold: float = 0.8,
        history_length: int = 240,
        raw_frame_storage: bool = False,
    ) -> None:
        self.detector = detector
        self.zones = zones
        self.camera_id = camera_id
        self.queue_threshold = queue_threshold
        self.raw_frame_storage = raw_frame_storage

        self.tracker = CentroidTracker(ttl_seconds=track_ttl_seconds)
        self.table_tracker = TableUsageTracker()
        self.heatmap = HeatmapGrid()
        self.occupancy_acc = OccupancyAccumulator()

        self._history: deque[dict] = deque(maxlen=history_length)
        self._hourly: dict[int, list[int]] = {}
        self._latest: dict | None = None
        self._latest_tables: list[dict] = []
        self._started_at = utcnow()

    @property
    def privacy_flags(self) -> dict[str, bool]:
        return {
            "identity_tracking": False,
            "biometrics": False,
            "facial_recognition": False,
            "demographic_inference": False,
            "emotion_detection": False,
            "audio_recording": False,
            "raw_frame_storage": self.raw_frame_storage,
        }

    def tick(self, frame=None, now: float | None = None) -> dict:
        """Run one detection + analytics cycle and return the live snapshot."""
        now = time.monotonic() if now is None else now

        detections = self.detector.detect(frame)
        foot_points = [d.foot_point for d in detections]
        centroids = [d.centroid for d in detections]

        # Ephemeral tracking — purely for short-term flow estimation.
        self.tracker.update(foot_points, now)

        occupancy = compute_occupancy(foot_points, self.zones)
        self.occupancy_acc.add(occupancy)

        queue = compute_queue_metrics(foot_points, self.zones)

        tables = self.table_tracker.update(foot_points, self.zones, now)
        self._latest_tables = [t.to_dict() for t in tables]

        self.heatmap.add_points(centroids)
        self.heatmap.step()

        ts = utcnow()
        self._record_hourly(ts.hour, occupancy.total)

        snapshot = {
            "timestamp": iso(ts),
            "camera_id": self.camera_id,
            "occupancy": occupancy.to_dict(),
            "queue": queue.to_dict(),
            "tables": self._latest_tables,
            "active_tracks": self.tracker.active_count(),
            "privacy": {
                "identity_tracking": False,
                "biometrics": False,
                "raw_frame_storage": self.raw_frame_storage,
            },
        }
        self._latest = snapshot
        self._history.append(
            {
                "timestamp": snapshot["timestamp"],
                "total": occupancy.total,
                "queue_count": queue.count,
                "queue_pressure": queue.pressure_score,
            }
        )
        return snapshot

    # -- read APIs --------------------------------------------------------
    def live(self) -> dict:
        if self._latest is None:
            return self.tick()
        return self._latest

    def history(self) -> list[dict]:
        return list(self._history)

    def heatmap_data(self) -> dict:
        return self.heatmap.to_dict()

    def queue_data(self) -> dict:
        return self.live().get("queue", {})

    def tables_data(self) -> dict:
        now = time.monotonic()
        return {
            "tables": self._latest_tables,
            "summary": self.table_tracker.summary(now),
        }

    def summary(self) -> dict:
        peak_hour = self._peak_hour()
        return {
            "camera_id": self.camera_id,
            "since": iso(self._started_at),
            "estimated_visitors": self.tracker.created_total,
            "occupancy": self.occupancy_acc.to_dict(),
            "peak_hour": peak_hour,
            "tables": self.table_tracker.summary(time.monotonic()),
            "privacy": self.privacy_flags,
        }

    # -- internals --------------------------------------------------------
    def _record_hourly(self, hour: int, total: int) -> None:
        self._hourly.setdefault(hour, []).append(total)
        # Keep each hour bucket bounded to avoid unbounded growth.
        if len(self._hourly[hour]) > 1800:
            self._hourly[hour] = self._hourly[hour][-1800:]

    def _peak_hour(self) -> str | None:
        if not self._hourly:
            return None
        best_hour = max(
            self._hourly,
            key=lambda h: sum(self._hourly[h]) / len(self._hourly[h]),
        )
        return f"{best_hour:02d}:00"
