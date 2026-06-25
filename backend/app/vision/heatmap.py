"""Spatial heatmap aggregation — anonymous density only.

The heatmap is a coarse grid over the camera's normalized field of view. Each
cell accumulates how often *any* anonymous point fell inside it. It encodes
**where crowds form**, never **who** was there. Cells are intentionally coarse
to prevent any attempt at pinpointing individuals.
"""

from __future__ import annotations

from app.utils.geometry import Point


class HeatmapGrid:
    """A decaying density grid over normalized ``[0, 1] x [0, 1]`` space.

    Args:
        rows: Number of grid rows.
        cols: Number of grid columns.
        decay: Multiplicative decay applied on each :meth:`step` so recent
            activity dominates. ``1.0`` disables decay.
    """

    def __init__(self, rows: int = 12, cols: int = 16, decay: float = 0.98) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("rows and cols must be >= 1")
        self.rows = rows
        self.cols = cols
        self.decay = decay
        self.cells: list[list[float]] = [[0.0] * cols for _ in range(rows)]

    def _cell_for(self, point: Point) -> tuple[int, int]:
        x = min(max(point[0], 0.0), 0.999999)
        y = min(max(point[1], 0.0), 0.999999)
        col = int(x * self.cols)
        row = int(y * self.rows)
        return row, col

    def add_point(self, point: Point, weight: float = 1.0) -> None:
        row, col = self._cell_for(point)
        self.cells[row][col] += weight

    def add_points(self, points: list[Point], weight: float = 1.0) -> None:
        for point in points:
            self.add_point(point, weight)

    def step(self) -> None:
        """Apply temporal decay (call once per processed frame/interval)."""
        if self.decay >= 1.0:
            return
        for r in range(self.rows):
            row = self.cells[r]
            for c in range(self.cols):
                row[c] *= self.decay

    def max_value(self) -> float:
        return max((max(row) for row in self.cells), default=0.0)

    def total(self) -> float:
        return sum(sum(row) for row in self.cells)

    def normalized(self) -> list[list[float]]:
        """Return the grid scaled to ``[0, 1]`` (max cell → 1.0)."""
        peak = self.max_value()
        if peak <= 0:
            return [[0.0] * self.cols for _ in range(self.rows)]
        return [[round(v / peak, 4) for v in row] for row in self.cells]

    def reset(self) -> None:
        self.cells = [[0.0] * self.cols for _ in range(self.rows)]

    def to_dict(self, normalize: bool = True) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "max": round(self.max_value(), 4),
            "cells": self.normalized() if normalize else self.cells,
        }
