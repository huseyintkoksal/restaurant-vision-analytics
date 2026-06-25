"""Optional OpenCV HOG person detector.

A lightweight, dependency-optional real-image detector based on OpenCV's classic
HOG + linear-SVM pedestrian descriptor. It detects anonymous person-shaped
regions only — it does **not** read faces, attributes, or identity.

OpenCV is an optional extra (``pip install ".[opencv]"``). Importing this module
without OpenCV installed is safe; constructing the detector raises a clear,
actionable error. No model weights are bundled or silently downloaded — the HOG
descriptor ships inside OpenCV itself.
"""

from __future__ import annotations

from app.vision.detector_base import Detection, Detector, DetectorInfo

try:
    import cv2 as _cv2

    _HAS_CV2 = True
except Exception:  # pragma: no cover - optional dependency
    _cv2 = None  # type: ignore[assignment]
    _HAS_CV2 = False


class OpenCVHOGDetector(Detector):
    """Anonymous person detector using OpenCV's built-in HOG descriptor.

    Args:
        hit_threshold: SVM decision threshold; higher → fewer detections.
        win_stride: Sliding-window stride in pixels.
        min_confidence: Minimum detection weight to keep.
    """

    def __init__(
        self,
        hit_threshold: float = 0.0,
        win_stride: tuple[int, int] = (8, 8),
        min_confidence: float = 0.3,
    ) -> None:
        if not _HAS_CV2:
            raise RuntimeError(
                "OpenCVHOGDetector requires OpenCV. Install with: pip install \".[opencv]\""
            )
        self.win_stride = win_stride
        self.hit_threshold = hit_threshold
        self.min_confidence = min_confidence
        self._hog = _cv2.HOGDescriptor()
        self._hog.setSVMDetector(_cv2.HOGDescriptor_getDefaultPeopleDetector())

    @property
    def info(self) -> DetectorInfo:
        return DetectorInfo(
            name="OpenCVHOGDetector",
            requires_model_download=False,
            notes="Classic HOG+SVM pedestrian detector bundled with OpenCV. Anonymous boxes only.",
        )

    def detect(self, frame) -> list[Detection]:
        """Return anonymous person detections for a BGR/grayscale numpy frame."""
        height, width = frame.shape[:2]
        rects, weights = self._hog.detectMultiScale(
            frame, winStride=self.win_stride, hitThreshold=self.hit_threshold
        )
        detections: list[Detection] = []
        for (x, y, w, h), weight in zip(rects, weights, strict=False):
            confidence = float(weight)
            if confidence < self.min_confidence:
                continue
            bbox = (
                x / width,
                y / height,
                (x + w) / width,
                (y + h) / height,
            )
            detections.append(
                Detection(bbox=bbox, confidence=min(confidence, 1.0), label="person")
            )
        return detections
