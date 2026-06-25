"""Zone membership and occupancy counting."""

from __future__ import annotations

from app.vision.occupancy import compute_occupancy
from app.vision.zones import Zone, ZoneType


def _zone(zone_id: str, ztype: ZoneType, x0, y0, x1, y1, capacity=None) -> Zone:
    return Zone(
        id=zone_id,
        name=zone_id,
        type=ztype,
        polygon=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        capacity=capacity,
    )


def test_zone_contains():
    entrance = _zone("entrance", ZoneType.ENTRANCE, 0.0, 0.0, 0.5, 0.5)
    assert entrance.contains((0.25, 0.25)) is True
    assert entrance.contains((0.75, 0.75)) is False


def test_occupancy_counts_per_zone():
    zones = [
        _zone("queue", ZoneType.QUEUE, 0.0, 0.0, 0.5, 1.0),
        _zone("dining", ZoneType.DINING_AREA, 0.5, 0.0, 1.0, 1.0),
    ]
    points = [(0.1, 0.5), (0.2, 0.5), (0.7, 0.5)]
    snap = compute_occupancy(points, zones)

    assert snap.by_zone["queue"] == 2
    assert snap.by_zone["dining"] == 1
    assert snap.total == 3
    assert snap.by_type["queue"] == 2
    assert snap.by_type["dining_area"] == 1


def test_occupancy_total_counts_each_point_once_in_overlap():
    # A nested table inside a dining area must not double-count its occupant.
    zones = [
        _zone("dining", ZoneType.DINING_AREA, 0.0, 0.0, 1.0, 1.0),
        _zone("table-1", ZoneType.TABLE, 0.4, 0.4, 0.6, 0.6),
    ]
    points = [(0.5, 0.5)]  # inside both dining and the table
    snap = compute_occupancy(points, zones)

    assert snap.by_zone["dining"] == 1
    assert snap.by_zone["table-1"] == 1
    assert snap.total == 1  # counted once overall


def test_occupancy_ignores_points_outside_all_zones():
    zones = [_zone("queue", ZoneType.QUEUE, 0.0, 0.0, 0.5, 1.0)]
    points = [(0.1, 0.5), (0.9, 0.9)]
    snap = compute_occupancy(points, zones)
    assert snap.total == 1
