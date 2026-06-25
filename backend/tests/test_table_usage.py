"""Table-usage analytics (occupied/free, dwell, turnover, idle)."""

from __future__ import annotations

from app.vision.table_usage import TableUsageTracker
from app.vision.zones import Zone, ZoneType


def _table(zone_id: str, x0=0.0, y0=0.0, x1=1.0, y1=1.0) -> Zone:
    return Zone(
        id=zone_id,
        name=zone_id,
        type=ZoneType.TABLE,
        polygon=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
    )


def test_table_starts_free():
    tracker = TableUsageTracker()
    readings = tracker.update([], [_table("t1")], now=0.0)
    assert readings[0].occupied is False
    assert readings[0].turnover_count == 0


def test_table_occupied_and_dwell_time():
    tracker = TableUsageTracker()
    table = _table("t1")
    tracker.update([(0.5, 0.5)], [table], now=0.0)
    readings = tracker.update([(0.5, 0.5)], [table], now=120.0)
    assert readings[0].occupied is True
    assert readings[0].duration_seconds == 120


def test_turnover_increments_on_vacate():
    tracker = TableUsageTracker()
    table = _table("t1")
    tracker.update([(0.5, 0.5)], [table], now=0.0)  # occupied
    tracker.update([(0.5, 0.5)], [table], now=60.0)  # still occupied
    readings = tracker.update([], [table], now=70.0)  # vacated
    assert readings[0].occupied is False
    assert readings[0].turnover_count == 1


def test_idle_table_detected_after_threshold():
    tracker = TableUsageTracker(idle_threshold_seconds=600.0)
    table = _table("t1")
    tracker.update([], [table], now=0.0)
    readings = tracker.update([], [table], now=601.0)
    assert readings[0].occupied is False
    assert readings[0].idle is True


def test_summary_reports_aggregates():
    tracker = TableUsageTracker()
    tables = [_table("t1", 0.0, 0.0, 0.5, 1.0), _table("t2", 0.5, 0.0, 1.0, 1.0)]
    tracker.update([(0.25, 0.5)], tables, now=0.0)  # t1 occupied, t2 free
    summary = tracker.summary(now=10.0)
    assert summary["tables"] == 2
    assert summary["occupied"] == 1
    assert summary["free"] == 1
