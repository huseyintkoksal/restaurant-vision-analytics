"""Queue pressure analytics."""

from __future__ import annotations

from app.vision.queue import compute_queue_metrics, queue_alert_triggered
from app.vision.zones import Zone, ZoneType


def _queue_zone(capacity: int) -> Zone:
    return Zone(
        id="queue-1",
        name="Queue",
        type=ZoneType.QUEUE,
        polygon=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
        capacity=capacity,
    )


def test_empty_queue_is_clear():
    metrics = compute_queue_metrics([], [_queue_zone(6)])
    assert metrics.count == 0
    assert metrics.pressure_score == 0.0
    assert metrics.status == "clear"


def test_queue_pressure_scales_with_count():
    zone = _queue_zone(10)
    points = [(0.5, 0.5)] * 5
    metrics = compute_queue_metrics(points, [zone])
    assert metrics.count == 5
    assert metrics.pressure_score == 0.5
    assert metrics.status == "moderate"


def test_queue_pressure_caps_at_one():
    zone = _queue_zone(4)
    points = [(0.5, 0.5)] * 12
    metrics = compute_queue_metrics(points, [zone])
    assert metrics.pressure_score == 1.0
    assert metrics.status == "congested"
    assert queue_alert_triggered(metrics, threshold=0.8) is True


def test_no_queue_zone_returns_clear():
    metrics = compute_queue_metrics([(0.5, 0.5)], [])
    assert metrics.status == "clear"
    assert metrics.pressure_score == 0.0
