"""Synthetic frame source (demo mode).

This source represents "no camera". It returns blank frames so the
pipeline shape is uniform, but in practice demo mode pairs it with the
:class:`~app.vision.mock_detector.SyntheticDetector`, which generates anonymous
detections directly and ignores frame content. No imagery is ever captured or
stored.
"""

from __future__ import annotations

from app.vision.sources.source_base import FrameSource, SourceInfo

try:
    import numpy as _np

    _HAS_NUMPY = True
except Exception:  # pragma: no cover
    _np = None  # type: ignore[assignment]
    _HAS_NUMPY = False


class SyntheticSource(FrameSource):
    """A camera-free source that yields blank frames."""

    def __init__(self, width: int = 640, height: int = 360) -> None:
        self.width = width
        self.height = height
        self._opened = False

    @property
    def info(self) -> SourceInfo:
        return SourceInfo(
            name="SyntheticSource",
            kind="synthetic",
            requires_opencv=False,
            experimental=False,
            notes="No camera. Pairs with SyntheticDetector, which drives analytics directly.",
        )

    def open(self) -> None:
        self._opened = True

    def is_opened(self) -> bool:
        return self._opened

    def read(self):
        if not self._opened:
            self.open()
        if _HAS_NUMPY:
            return _np.zeros((self.height, self.width, 3), dtype=_np.uint8)
        # numpy-free fallback: a nested-list frame.
        return [[[0, 0, 0]] * self.width for _ in range(self.height)]

    def release(self) -> None:
        self._opened = False
