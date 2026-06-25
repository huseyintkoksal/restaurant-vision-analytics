"""Frame-source interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

# A frame is an opaque array-like (e.g. a numpy BGR image). The source layer
# never inspects pixels for personal attributes.
Frame = Any


@dataclass
class SourceInfo:
    """Static metadata describing a frame source."""

    name: str
    kind: str  # synthetic | video_file | rtsp | device
    requires_opencv: bool
    experimental: bool = False
    notes: str = ""


class FrameSource(ABC):
    """Abstract base class for frame sources.

    Implementations supply frames to a detector. They must not store raw frames
    or extract any personal attribute.
    """

    @property
    @abstractmethod
    def info(self) -> SourceInfo:
        """Return static metadata about this source."""

    @abstractmethod
    def open(self) -> None:
        """Acquire the underlying resource (file handle, stream, etc.)."""

    @abstractmethod
    def read(self) -> Frame | None:
        """Return the next frame, or ``None`` when no frame is available."""

    def is_opened(self) -> bool:  # pragma: no cover - trivial default
        return True

    def release(self) -> None:  # pragma: no cover - optional hook
        """Release any held resources."""
        return None

    def __enter__(self) -> FrameSource:
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.release()
