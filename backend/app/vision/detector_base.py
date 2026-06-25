"""Detector interface and the anonymous :class:`Detection` value object.

A :class:`Detection` describes **where** an anonymous person-shaped region is in
the frame — nothing about **who** it is. There is deliberately no field for
identity, face, gait, clothing colour, embedding, age, gender, or any other
personal attribute. Detectors are pluggable so that the analytics layer never
depends on a specific model.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

# A frame is an opaque object to this layer (e.g. a numpy array). The base
# layer never inspects pixel content for personal attributes.
Frame = Any


@dataclass(frozen=True)
class Detection:
    """An anonymous person-shaped detection in normalized image space.

    Attributes:
        bbox: ``(x1, y1, x2, y2)`` in normalized coordinates (0.0–1.0).
        confidence: Detector confidence in ``[0, 1]``.
        label: Always ``"person"``. Present only to make the schema explicit;
            no sub-classification (age/gender/etc.) is ever produced.
    """

    bbox: tuple[float, float, float, float]
    confidence: float = 1.0
    label: str = "person"

    @property
    def centroid(self) -> tuple[float, float]:
        """Geometric center of the bounding box (used for heatmaps)."""
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @property
    def foot_point(self) -> tuple[float, float]:
        """Bottom-center of the box — best proxy for floor position / zone."""
        x1, _y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, y2)


@dataclass
class DetectorInfo:
    """Static metadata describing a detector implementation."""

    name: str
    requires_model_download: bool = False
    notes: str = ""
    extras: dict[str, Any] = field(default_factory=dict)


class Detector(ABC):
    """Abstract base class for all detectors.

    Implementations must return a list of :class:`Detection` objects for a given
    frame. They must **not** return identity, biometric, or demographic data.
    """

    @property
    @abstractmethod
    def info(self) -> DetectorInfo:
        """Return static metadata about this detector."""

    @abstractmethod
    def detect(self, frame: Frame) -> list[Detection]:
        """Return anonymous person detections for a single frame."""

    def close(self) -> None:  # pragma: no cover - optional hook
        """Release any resources held by the detector (optional)."""
        return None
