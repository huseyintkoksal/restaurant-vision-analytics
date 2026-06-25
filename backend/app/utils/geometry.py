"""Pure-Python 2D geometry helpers used by the zone engine.

No third-party dependencies: coordinates are plain ``(x, y)`` float tuples in
normalized image space (0.0–1.0) or pixel space — the functions are unit
agnostic. Kept dependency-free so the geometry tests run anywhere.
"""

from __future__ import annotations

from collections.abc import Sequence

Point = tuple[float, float]
Polygon = Sequence[Point]


def point_in_polygon(point: Point, polygon: Polygon) -> bool:
    """Return ``True`` if ``point`` lies inside ``polygon``.

    Uses the classic ray-casting (even-odd rule) algorithm. Points exactly on
    an edge are treated as inside, which is the desired behaviour for zone
    occupancy where a boundary detection should count as "in the zone".

    Args:
        point: The ``(x, y)`` point to test.
        polygon: An ordered sequence of ``(x, y)`` vertices. The polygon is
            implicitly closed (last vertex connects to the first).
    """
    if len(polygon) < 3:
        return False

    x, y = point
    inside = False
    n = len(polygon)

    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        # On-edge check (treat boundary as inside).
        if _point_on_segment(point, polygon[i], polygon[j]):
            return True

        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i

    return inside


def _point_on_segment(p: Point, a: Point, b: Point, eps: float = 1e-9) -> bool:
    """Return ``True`` if ``p`` lies on the segment ``a``–``b``."""
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if abs(cross) > eps:
        return False
    dot = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    if dot < -eps:
        return False
    squared_len = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return dot <= squared_len + eps


def polygon_area(polygon: Polygon) -> float:
    """Return the (absolute) area of a simple polygon via the shoelace formula."""
    if len(polygon) < 3:
        return 0.0
    area = 0.0
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def polygon_centroid(polygon: Polygon) -> Point:
    """Return the centroid (geometric center) of a polygon.

    Falls back to the average of the vertices for degenerate (zero-area)
    polygons.
    """
    n = len(polygon)
    if n == 0:
        raise ValueError("polygon must have at least one vertex")
    if n < 3:
        return _vertex_average(polygon)

    area = 0.0
    cx = 0.0
    cy = 0.0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        area += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross

    area *= 0.5
    if abs(area) < 1e-12:
        return _vertex_average(polygon)

    return (cx / (6.0 * area), cy / (6.0 * area))


def _vertex_average(polygon: Polygon) -> Point:
    n = len(polygon)
    sx = sum(p[0] for p in polygon)
    sy = sum(p[1] for p in polygon)
    return (sx / n, sy / n)


def bounding_box(polygon: Polygon) -> tuple[float, float, float, float]:
    """Return ``(min_x, min_y, max_x, max_y)`` for a polygon."""
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return (min(xs), min(ys), max(xs), max(ys))


def euclidean_distance(a: Point, b: Point) -> float:
    """Return the Euclidean distance between two points."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
