"""Spatial heatmap aggregation."""

from __future__ import annotations

from app.vision.heatmap import HeatmapGrid


def test_point_maps_to_expected_cell():
    grid = HeatmapGrid(rows=10, cols=10, decay=1.0)
    grid.add_point((0.05, 0.05))  # top-left cell
    assert grid.cells[0][0] == 1.0
    grid.add_point((0.95, 0.95))  # bottom-right cell
    assert grid.cells[9][9] == 1.0


def test_normalized_peaks_at_one():
    grid = HeatmapGrid(rows=4, cols=4, decay=1.0)
    grid.add_points([(0.1, 0.1)] * 5)
    grid.add_point((0.9, 0.9))
    normalized = grid.normalized()
    assert max(max(row) for row in normalized) == 1.0
    assert grid.max_value() == 5.0


def test_decay_reduces_values():
    grid = HeatmapGrid(rows=2, cols=2, decay=0.5)
    grid.add_point((0.25, 0.25))
    grid.step()
    assert grid.cells[0][0] == 0.5


def test_to_dict_shape():
    grid = HeatmapGrid(rows=3, cols=5)
    grid.add_point((0.5, 0.5))
    data = grid.to_dict()
    assert data["rows"] == 3
    assert data["cols"] == 5
    assert len(data["cells"]) == 3
    assert all(len(row) == 5 for row in data["cells"])


def test_heatmap_holds_density_not_identity():
    # The grid stores only floats — there is nowhere to put an identity.
    grid = HeatmapGrid(rows=2, cols=2)
    grid.add_points([(0.1, 0.1), (0.9, 0.9)])
    for row in grid.cells:
        for value in row:
            assert isinstance(value, float)
