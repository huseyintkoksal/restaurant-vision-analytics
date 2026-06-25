"""Frame sources — pluggable input layer for the vision pipeline.

A :class:`FrameSource` supplies frames to a *real* detector. Demo mode does not
need one: the :class:`~app.vision.mock_detector.SyntheticDetector` drives the
analytics itself. Real sources (video file, RTSP/device) are **optional and
experimental** in v0.1 and require OpenCV.

Privacy notes that apply to every source:

* Camera credentials come from environment variables, never from committed code.
* Raw frames are not persisted by default (``ENABLE_RAW_FRAME_STORAGE=false``).
* No source extracts identity, biometrics, or demographic attributes.
"""

from app.vision.sources.opencv_stream_source import OpenCVStreamSource
from app.vision.sources.source_base import FrameSource, SourceInfo
from app.vision.sources.synthetic_source import SyntheticSource
from app.vision.sources.video_file_source import VideoFileSource

__all__ = [
    "FrameSource",
    "SourceInfo",
    "SyntheticSource",
    "VideoFileSource",
    "OpenCVStreamSource",
    "create_source",
]


def create_source(camera_source: str | None, demo_mode: bool = True) -> FrameSource:
    """Return an appropriate :class:`FrameSource` for the configuration.

    Selection rules (kept deliberately simple):

    * demo mode, or no ``camera_source`` → :class:`SyntheticSource`.
    * an ``rtsp://``/``http://`` URL or a numeric device index →
      :class:`OpenCVStreamSource`.
    * anything else (a path) → :class:`VideoFileSource`.

    The real sources are constructed lazily; OpenCV is only required when you
    actually :meth:`~FrameSource.open` them.
    """
    if demo_mode or not camera_source:
        return SyntheticSource()

    lowered = camera_source.lower()
    if lowered.startswith(("rtsp://", "http://", "https://")) or camera_source.isdigit():
        return OpenCVStreamSource(camera_source)
    return VideoFileSource(camera_source)
