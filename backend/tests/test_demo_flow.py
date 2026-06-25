"""Synthetic (demo) data generation.

Verifies that demo mode produces realistic, time-varying analytics without any
camera — and that the detector only ever emits anonymous person boxes.
"""

from __future__ import annotations

from app.database.init_db import default_demo_zones
from app.vision.analytics_engine import AnalyticsEngine
from app.vision.detector_base import Detection
from app.vision.mock_detector import MockDetector, SyntheticDetector


def test_mock_is_synthetic_alias():
    assert MockDetector is SyntheticDetector


def test_detector_emits_only_anonymous_person_boxes():
    detector = SyntheticDetector(seed=3, base_arrival_rate=60)
    saw_detection = False
    for _ in range(60):
        detections = detector.detect()
        for det in detections:
            saw_detection = True
            assert isinstance(det, Detection)
            assert det.label == "person"
            x1, y1, x2, y2 = det.bbox
            assert 0.0 <= x1 <= 1.0 and 0.0 <= y1 <= 1.0
            assert 0.0 <= x2 <= 1.0 and 0.0 <= y2 <= 1.0
            assert 0.0 <= det.confidence <= 1.0
    assert saw_detection, "synthetic detector should produce detections over time"


def test_demo_flow_drives_occupancy_and_tables():
    zones = [z.to_runtime() for z in default_demo_zones()]
    engine = AnalyticsEngine(
        detector=SyntheticDetector(seed=3, base_arrival_rate=60),
        zones=zones,
    )

    max_occupancy = 0
    table_was_occupied = False
    for _ in range(200):
        snap = engine.tick()
        max_occupancy = max(max_occupancy, snap["occupancy"]["total"])
        if any(t["occupied"] for t in snap["tables"]):
            table_was_occupied = True

    assert max_occupancy >= 1
    assert table_was_occupied
    # Estimated visitors accumulate as anonymous tracks come and go.
    assert engine.summary()["estimated_visitors"] >= 1
