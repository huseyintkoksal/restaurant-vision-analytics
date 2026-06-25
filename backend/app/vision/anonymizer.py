"""Privacy anonymizer for optional debug frames.

The toolkit does **not** store raw frames by default. When an operator
explicitly enables debug imagery, every detected person-shaped region is
blurred or masked *before* the frame leaves memory. These helpers make the
privacy-preserving path the easy, default path.

``numpy`` is required only for the pixel operations here; importing this module
never fails if it is missing, so the rest of the pipeline stays dependency-light.
"""

from __future__ import annotations

from app.config import Settings
from app.vision.detector_base import Detection

try:  # numpy is a core dependency but guard so imports never hard-fail.
    import numpy as _np

    _HAS_NUMPY = True
except Exception:  # pragma: no cover - environment without numpy
    _np = None  # type: ignore[assignment]
    _HAS_NUMPY = False

try:  # OpenCV is fully optional.
    import cv2 as _cv2

    _HAS_CV2 = True
except Exception:  # pragma: no cover - optional dependency
    _cv2 = None  # type: ignore[assignment]
    _HAS_CV2 = False


class AnonymizationError(RuntimeError):
    """Raised when anonymization is requested but numpy is unavailable."""


def _require_numpy() -> None:
    if not _HAS_NUMPY:
        raise AnonymizationError(
            "numpy is required for frame anonymization. Install with: pip install numpy"
        )


def _denormalize_box(
    bbox: tuple[float, float, float, float], width: int, height: int
) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = bbox
    return (
        max(0, int(x1 * width)),
        max(0, int(y1 * height)),
        min(width, int(x2 * width)),
        min(height, int(y2 * height)),
    )


def mask_regions(frame, detections: list[Detection], color: tuple[int, int, int] = (32, 32, 32)):
    """Return a copy of ``frame`` with every detection region filled solid.

    This is the strongest and cheapest anonymization: no facial or bodily detail
    survives.
    """
    _require_numpy()
    height, width = frame.shape[:2]
    out = frame.copy()
    for det in detections:
        x1, y1, x2, y2 = _denormalize_box(det.bbox, width, height)
        if x2 > x1 and y2 > y1:
            out[y1:y2, x1:x2] = color
    return out


def blur_regions(frame, detections: list[Detection], strength: int = 25):
    """Return a copy of ``frame`` with every detection region heavily blurred.

    Uses OpenCV's Gaussian blur when available, otherwise a numpy box-average
    fallback. Either way enough detail is destroyed to prevent identification.
    """
    _require_numpy()
    height, width = frame.shape[:2]
    out = frame.copy()
    for det in detections:
        x1, y1, x2, y2 = _denormalize_box(det.bbox, width, height)
        if x2 <= x1 or y2 <= y1:
            continue
        region = out[y1:y2, x1:x2]
        out[y1:y2, x1:x2] = _blur_region(region, strength)
    return out


def _blur_region(region, strength: int):
    if _HAS_CV2:
        k = max(3, strength | 1)  # kernel size must be odd
        return _cv2.GaussianBlur(region, (k, k), 0)
    # numpy-only fallback: downsample then upsample to destroy detail.
    factor = max(2, strength // 4)
    h, w = region.shape[:2]
    small = region[::factor, ::factor]
    return _np.kron(small, _np.ones((factor, factor, 1), dtype=region.dtype))[:h, :w]


def anonymize_frame(frame, detections: list[Detection], mode: str = "blur"):
    """Apply the configured anonymization to all detections.

    Args:
        mode: ``"blur"`` (default) or ``"mask"``.
    """
    if mode == "mask":
        return mask_regions(frame, detections)
    return blur_regions(frame, detections)


def may_store_raw_frame(settings: Settings) -> bool:
    """Single source of truth for the raw-frame policy.

    Returns ``True`` only when an operator has explicitly opted in. The rest of
    the codebase must route raw-frame writes through this gate.
    """
    return bool(settings.enable_raw_frame_storage)
