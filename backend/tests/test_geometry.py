"""Geometry primitives used by the zone engine."""

from __future__ import annotations

import pytest

from app.utils.geometry import (
    bounding_box,
    euclidean_distance,
    point_in_polygon,
    polygon_area,
    polygon_centroid,
)

SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
TRIANGLE = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]


def test_point_inside_polygon():
    assert point_in_polygon((0.5, 0.5), SQUARE) is True
    assert point_in_polygon((0.5, 0.25), TRIANGLE) is True


def test_point_outside_polygon():
    assert point_in_polygon((2.0, 2.0), SQUARE) is False
    assert point_in_polygon((-0.1, 0.5), SQUARE) is False
    assert point_in_polygon((0.95, 0.95), TRIANGLE) is False


def test_point_on_edge_counts_as_inside():
    assert point_in_polygon((0.5, 0.0), SQUARE) is True  # on bottom edge
    assert point_in_polygon((0.0, 0.0), SQUARE) is True  # on a corner


def test_degenerate_polygon_is_never_inside():
    assert point_in_polygon((0.0, 0.0), [(0.0, 0.0), (1.0, 1.0)]) is False


def test_polygon_area_and_centroid():
    assert polygon_area(SQUARE) == pytest.approx(1.0)
    cx, cy = polygon_centroid(SQUARE)
    assert cx == pytest.approx(0.5)
    assert cy == pytest.approx(0.5)


def test_bounding_box_and_distance():
    assert bounding_box(SQUARE) == (0.0, 0.0, 1.0, 1.0)
    assert euclidean_distance((0.0, 0.0), (3.0, 4.0)) == pytest.approx(5.0)
