"""RTSP / device stream frame source (experimental).

Reads frames from an RTSP/HTTP stream or a local capture device via OpenCV.

Security & privacy:

* **Credentials come from the environment**, e.g. ``CAMERA_SOURCE`` — never from
  committed code. Do not embed passwords in URLs you commit.
* Raw frames are not persisted by default.
* This source detects anonymous person regions only; it performs no facial
  recognition, biometrics, or identity tracking.

OpenCV is optional: importing this module is always safe; opening the stream
without OpenCV raises a clear error.
"""

from __future__ import annotations

from app.vision.sources.source_base import FrameSource, SourceInfo

try:
    import cv2 as _cv2

    _HAS_CV2 = True
except Exception:  # pragma: no cover - optional dependency
    _cv2 = None  # type: ignore[assignment]
    _HAS_CV2 = False


class OpenCVStreamSource(FrameSource):
    """Frame source backed by an RTSP/HTTP stream or a device index.

    Args:
        source: An ``rtsp://``/``http://`` URL or a numeric device index (as a
            string, e.g. ``"0"``). Prefer passing this via an environment
            variable so credentials never enter version control.
    """

    def __init__(self, source: str) -> None:
        self.source = source
        self._cap = None

    @property
    def info(self) -> SourceInfo:
        kind = "device" if self.source.isdigit() else "rtsp"
        return SourceInfo(
            name="OpenCVStreamSource",
            kind=kind,
            requires_opencv=True,
            experimental=True,
            notes="RTSP/HTTP stream or capture device via OpenCV. Credentials from env only.",
        )

    def _target(self):
        return int(self.source) if self.source.isdigit() else self.source

    def open(self) -> None:
        if not _HAS_CV2:
            raise RuntimeError(
                "OpenCVStreamSource requires OpenCV. Install with: pip install \".[opencv]\""
            )
        self._cap = _cv2.VideoCapture(self._target())
        if not self._cap.isOpened():
            # Avoid echoing the (possibly credentialed) source string verbatim.
            raise RuntimeError("Could not open camera stream (check source and network).")

    def is_opened(self) -> bool:
        return self._cap is not None and self._cap.isOpened()

    def read(self):
        if self._cap is None:
            self.open()
        ok, frame = self._cap.read()
        if not ok:
            return None
        return frame

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
