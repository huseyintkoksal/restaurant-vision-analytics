"""Analytics snapshot schema (engine output, API, and persistence)."""

from __future__ import annotations

from sqlmodel import Session

from app.database.session import get_engine
from app.models.analytics_snapshot import AnalyticsSnapshot
from app.services.analytics_service import AnalyticsService

REQUIRED_TOP_LEVEL = {"timestamp", "camera_id", "occupancy", "queue", "tables", "privacy"}


def test_engine_snapshot_has_required_schema():
    snapshot = AnalyticsService().tick_once()
    assert REQUIRED_TOP_LEVEL.issubset(snapshot.keys())
    assert {"total", "by_zone"}.issubset(snapshot["occupancy"].keys())
    assert {"count", "pressure_score", "status"}.issubset(snapshot["queue"].keys())
    assert isinstance(snapshot["tables"], list)


def test_live_endpoint_schema(client):
    body = client.get("/api/analytics/live").json()
    assert REQUIRED_TOP_LEVEL.issubset(body.keys())
    assert body["privacy"]["identity_tracking"] is False


def test_summary_endpoint_schema(client):
    body = client.get("/api/analytics/summary").json()
    assert "estimated_visitors" in body
    assert "occupancy" in body
    assert body["privacy"]["facial_recognition"] is False


def test_heatmap_endpoint_schema(client):
    body = client.get("/api/analytics/heatmap").json()
    assert {"rows", "cols", "cells"}.issubset(body.keys())


def test_snapshot_model_roundtrips_payload():
    with Session(get_engine()) as session:
        snap = AnalyticsSnapshot(
            camera_id="demo-camera-1",
            total_occupancy=12,
            queue_count=4,
            queue_pressure=0.66,
            payload={"occupancy": {"total": 12}, "queue": {"count": 4}},
        )
        session.add(snap)
        session.commit()
        session.refresh(snap)
        assert snap.id is not None
        assert snap.payload["occupancy"]["total"] == 12
