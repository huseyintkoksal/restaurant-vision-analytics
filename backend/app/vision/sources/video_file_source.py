"""Video-file frame source (experimental).

Reads frames from a local video file via OpenCV. Useful for evaluating the
pipeline against recorded footage **you own and are permitted to use** — never
ship real customer video in this repository.

OpenCV is optional: importing this module is always safe; constructing/opening
the source without OpenCV raises a clear error.
"""

from __future__ import annotations

from app.vision.sources.source_base import FrameSource, SourceInfo

try:
    import cv2 as _cv2

    _HAS_CV2 = True
except Exception:  # pragma: no cover - optional dependency
    _cv2 = None  # type: ignore[assignment]
    _HAS_CV2 = False


class VideoFileSource(FrameSource):
    """Frame source backed by a local video file.

    Args:
        path: Path to a video file.
        loop: Restart from the beginning when the file ends (useful for demos).
    """

    def __init__(self, path: str, loop: bool = True) -> None:
        self.path = path
        self.loop = loop
        self._cap = None

    @property
    def info(self) -> SourceInfo:
        return SourceInfo(
            name="VideoFileSource",
            kind="video_file",
            requires_opencv=True,
            experimental=True,
            notes="Reads frames from a local video file via OpenCV.",
        )

    def open(self) -> None:
        if not _HAS_CV2:
            raise RuntimeError(
                "VideoFileSource requires OpenCV. Install with: pip install \".[opencv]\""
            )
        self._cap = _cv2.VideoCapture(self.path)
        if not self._cap.isOpened():
            raise RuntimeError(f"Could not open video file: {self.path}")

    def is_opened(self) -> bool:
        return self._cap is not None and self._cap.isOpened()

    def read(self):
        if self._cap is None:
            self.open()
        ok, frame = self._cap.read()
        if not ok:
            if self.loop:
                self._cap.set(_cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = self._cap.read()
                if ok:
                    return frame
            return None
        return frame

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
