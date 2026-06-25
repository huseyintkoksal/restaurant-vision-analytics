"""Zone definitions and point-in-zone helpers.

A *zone* is a named polygon over the camera's field of view (e.g. the queue
area, a table, the entrance). Zones are configuration objects — they describe
*places*, never people.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.utils.geometry import Point, Polygon, point_in_polygon, polygon_centroid


class ZoneType(StrEnum):
    """Supported zone categories for restaurant floor layouts."""

    ENTRANCE = "entrance"
    DINING_AREA = "dining_area"
    TABLE = "table"
    QUEUE = "queue"
    CASHIER = "cashier"
    KITCHEN_PASS = "kitchen_pass"
    PICKUP_AREA = "pickup_area"


@dataclass
class Zone:
    """A named polygonal region of interest.

    Attributes:
        id: Stable identifier for the zone (configuration id, not a person id).
        name: Human-readable label shown in the dashboard.
        type: One of :class:`ZoneType`.
        polygon: Ordered ``(x, y)`` vertices in normalized coordinates.
        capacity: Optional soft capacity used for occupancy thresholds.
        metadata: Free-form, non-personal configuration (e.g. table seats).
    """

    id: str
    name: str
    type: ZoneType
    polygon: Polygon
    capacity: int | None = None
    metadata: dict = field(default_factory=dict)

    def contains(self, point: Point) -> bool:
        """Return ``True`` if ``point`` lies within this zone's polygon."""
        return point_in_polygon(point, self.polygon)

    @property
    def centroid(self) -> Point:
        return polygon_centroid(self.polygon)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "polygon": [list(p) for p in self.polygon],
            "capacity": self.capacity,
            "metadata": self.metadata,
        }


def assign_points_to_zones(
    points: list[Point], zones: list[Zone]
) -> dict[str, list[int]]:
    """Map each zone id to the indices of ``points`` that fall inside it.

    A point may belong to multiple overlapping zones (e.g. a ``table`` nested
    inside a ``dining_area``). The caller decides how to combine them.
    """
    result: dict[str, list[int]] = {zone.id: [] for zone in zones}
    for idx, point in enumerate(points):
        for zone in zones:
            if zone.contains(point):
                result[zone.id].append(idx)
    return result


def zones_of_type(zones: list[Zone], zone_type: ZoneType) -> list[Zone]:
    """Return the subset of ``zones`` matching ``zone_type``."""
    return [z for z in zones if z.type == zone_type]
