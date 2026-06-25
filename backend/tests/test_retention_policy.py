"""Data-retention pruning."""

from __future__ import annotations

from datetime import timedelta

from sqlmodel import Session, select

from app.database.session import get_engine
from app.models.alert import Alert, AlertType
from app.models.analytics_snapshot import AnalyticsSnapshot
from app.services.retention_service import RetentionService
from app.utils.time import utcnow


def test_prune_removes_old_records_only():
    now = utcnow()
    old = now - timedelta(days=30)
    recent = now - timedelta(days=1)

    with Session(get_engine()) as session:
        session.add(
            AnalyticsSnapshot(camera_id="c1", total_occupancy=5, timestamp=old)
        )
        session.add(
            AnalyticsSnapshot(camera_id="c1", total_occupancy=7, timestamp=recent)
        )
        session.add(
            Alert(type=AlertType.queue_too_long, message="old", created_at=old)
        )
        session.commit()

    with Session(get_engine()) as session:
        result = RetentionService(retention_days=7).prune(session)

    assert result["snapshots_deleted"] >= 1
    assert result["alerts_deleted"] >= 1

    with Session(get_engine()) as session:
        remaining = session.exec(select(AnalyticsSnapshot)).all()
        # The recent snapshot must still be present.
        assert any(s.total_occupancy == 7 for s in remaining)
        # No snapshot older than the window should remain. SQLite returns naive
        # datetimes, so compare against a naive cutoff to avoid a tz mismatch.
        cutoff = (utcnow() - timedelta(days=7)).replace(tzinfo=None)
        assert all(s.timestamp.replace(tzinfo=None) >= cutoff for s in remaining)


def test_zero_retention_keeps_everything():
    # retention_days <= 0 disables pruning.
    with Session(get_engine()) as session:
        before = len(session.exec(select(AnalyticsSnapshot)).all())
        result = RetentionService(retention_days=0).prune(session)
        after = len(session.exec(select(AnalyticsSnapshot)).all())
    assert result["snapshots_deleted"] == 0
    assert before == after
