"""Occupancy analytics — anonymous person *counts* per zone.

These functions only ever count anonymous points. They produce aggregate
numbers (totals, per-zone counts, peaks, averages) and never anything tied to an
individual.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.utils.geometry import Point
from app.vision.zones import Zone, ZoneType


@dataclass
class OccupancySnapshot:
    """A single point-in-time occupancy reading."""

    total: int
    by_zone: dict[str, int]
    by_type: dict[str, int]

    def to_dict(self) -> dict:
        return {"total": self.total, "by_zone": self.by_zone, "by_type": self.by_type}


def compute_occupancy(points: list[Point], zones: list[Zone]) -> OccupancySnapshot:
    """Count anonymous points falling inside each zone.

    The *total* is the number of distinct points that fall inside at least one
    non-``table`` "presence" zone, falling back to the overall point count when
    no such zones are defined. This avoids double-counting a person who is both
    in a ``dining_area`` and a nested ``table``.
    """
    by_zone: dict[str, int] = {zone.id: 0 for zone in zones}
    by_type: dict[str, int] = {}

    for point in points:
        for zone in zones:
            if zone.contains(point):
                by_zone[zone.id] += 1
                by_type[zone.type.value] = by_type.get(zone.type.value, 0) + 1

    total = _distinct_total(points, zones)
    return OccupancySnapshot(total=total, by_zone=by_zone, by_type=by_type)


def _distinct_total(points: list[Point], zones: list[Zone]) -> int:
    """Count points present in any zone, each point at most once."""
    if not zones:
        return len(points)
    count = 0
    for point in points:
        if any(zone.contains(point) for zone in zones):
            count += 1
    return count


@dataclass
class OccupancyAccumulator:
    """Tracks peak and running-average occupancy across snapshots in a session.

    Stateful but *aggregate-only* — it stores numbers, never identities.
    """

    peak: int = 0
    _sum: int = 0
    _samples: int = 0
    peak_by_zone: dict[str, int] = field(default_factory=dict)

    def add(self, snapshot: OccupancySnapshot) -> None:
        self.peak = max(self.peak, snapshot.total)
        self._sum += snapshot.total
        self._samples += 1
        for zone_id, count in snapshot.by_zone.items():
            self.peak_by_zone[zone_id] = max(self.peak_by_zone.get(zone_id, 0), count)

    @property
    def average(self) -> float:
        if self._samples == 0:
            return 0.0
        return round(self._sum / self._samples, 2)

    def to_dict(self) -> dict:
        return {
            "peak": self.peak,
            "average": self.average,
            "samples": self._samples,
            "peak_by_zone": self.peak_by_zone,
        }


def capacity_utilization(snapshot: OccupancySnapshot, zones: list[Zone]) -> float | None:
    """Return overall capacity utilization (0–1) across capacity-bearing zones.

    Returns ``None`` when no zone declares a capacity.
    """
    relevant = [
        z for z in zones if z.capacity and z.type in (ZoneType.DINING_AREA, ZoneType.QUEUE)
    ]
    total_capacity = sum(z.capacity or 0 for z in relevant)
    if total_capacity <= 0:
        return None
    occupied = sum(snapshot.by_zone.get(z.id, 0) for z in relevant)
    return round(min(occupied / total_capacity, 1.0), 3)
