"""Queue analytics — anonymous crowd pressure in queue zones.

We never identify who is queuing or how long a *specific person* waited. We
estimate aggregate pressure from the number of anonymous points inside queue
zones, normalized against a configurable comfortable capacity.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.utils.geometry import Point
from app.vision.zones import Zone, ZoneType, zones_of_type


@dataclass
class QueueMetrics:
    """Aggregate queue metrics for one or more queue zones."""

    count: int
    pressure_score: float
    status: str
    estimated_wait_pressure: str

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "pressure_score": self.pressure_score,
            "status": self.status,
            "estimated_wait_pressure": self.estimated_wait_pressure,
        }


def _status_for(score: float) -> str:
    if score < 0.25:
        return "clear"
    if score < 0.55:
        return "moderate"
    if score < 0.8:
        return "busy"
    return "congested"


def _wait_pressure_for(score: float) -> str:
    if score < 0.25:
        return "low"
    if score < 0.55:
        return "medium"
    if score < 0.8:
        return "high"
    return "very_high"


def compute_queue_metrics(
    points: list[Point],
    zones: list[Zone],
    comfortable_capacity: int = 6,
) -> QueueMetrics:
    """Estimate queue pressure from anonymous points inside queue zones.

    Args:
        points: Anonymous foot points for the current frame.
        zones: All configured zones (queue zones are selected internally).
        comfortable_capacity: Number of people a queue can hold before it is
            considered fully "pressured" (score → 1.0). Per-zone ``capacity``
            overrides this when set.
    """
    queue_zones = zones_of_type(zones, ZoneType.QUEUE)
    if not queue_zones:
        return QueueMetrics(0, 0.0, "clear", "low")

    count = 0
    capacity_total = 0
    for zone in queue_zones:
        zone_capacity = zone.capacity or comfortable_capacity
        capacity_total += zone_capacity
        count += sum(1 for p in points if zone.contains(p))

    capacity_total = max(capacity_total, 1)
    pressure = round(min(count / capacity_total, 1.0), 3)
    return QueueMetrics(
        count=count,
        pressure_score=pressure,
        status=_status_for(pressure),
        estimated_wait_pressure=_wait_pressure_for(pressure),
    )


def queue_alert_triggered(metrics: QueueMetrics, threshold: float = 0.8) -> bool:
    """Return ``True`` when queue pressure crosses the alerting threshold."""
    return metrics.pressure_score >= threshold
