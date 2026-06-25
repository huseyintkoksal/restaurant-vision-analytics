"""Frame-source layer: selection, synthetic frames, and graceful OpenCV errors."""

from __future__ import annotations

import pytest

from app.vision.sources import (
    OpenCVStreamSource,
    SyntheticSource,
    VideoFileSource,
    create_source,
)
from app.vision.sources.opencv_stream_source import _HAS_CV2


def test_demo_mode_selects_synthetic_source():
    src = create_source(camera_source=None, demo_mode=True)
    assert isinstance(src, SyntheticSource)
    assert src.info.kind == "synthetic"
    assert src.info.requires_opencv is False


def test_factory_picks_stream_for_rtsp_and_device():
    assert isinstance(create_source("rtsp://host/stream", demo_mode=False), OpenCVStreamSource)
    assert isinstance(create_source("0", demo_mode=False), OpenCVStreamSource)


def test_factory_picks_video_file_for_path():
    assert isinstance(create_source("/footage/clip.mp4", demo_mode=False), VideoFileSource)


def test_synthetic_source_yields_blank_frame():
    with SyntheticSource(width=64, height=32) as src:
        frame = src.read()
    assert frame is not None
    # numpy array (default) exposes .shape; the fallback is a nested list.
    if hasattr(frame, "shape"):
        assert frame.shape == (32, 64, 3)
    else:  # pragma: no cover - numpy-free fallback
        assert len(frame) == 32


def test_real_sources_are_experimental_metadata():
    assert OpenCVStreamSource("rtsp://x").info.experimental is True
    assert VideoFileSource("x.mp4").info.experimental is True


@pytest.mark.skipif(_HAS_CV2, reason="OpenCV installed; graceful-error path not applicable")
def test_opencv_sources_raise_clear_error_without_cv2():
    with pytest.raises(RuntimeError, match="OpenCV"):
        VideoFileSource("x.mp4").open()
    with pytest.raises(RuntimeError, match="OpenCV"):
        OpenCVStreamSource("rtsp://x").open()
