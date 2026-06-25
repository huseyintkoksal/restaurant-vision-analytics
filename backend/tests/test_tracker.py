"""Ephemeral tracker behaviour: TTL expiry and no re-identification."""

from __future__ import annotations

from app.utils.ids import reset_track_counter
from app.vision.tracker import CentroidTracker


def test_track_created_and_followed():
    reset_track_counter()
    tracker = CentroidTracker(ttl_seconds=5.0, max_match_distance=0.2)
    tracker.update([(0.5, 0.5)], now=0.0)
    assert tracker.active_count() == 1
    first_id = tracker.tracks[0].id

    # A nearby point on the next frame should keep the same ephemeral id.
    tracker.update([(0.52, 0.5)], now=1.0)
    assert tracker.active_count() == 1
    assert tracker.tracks[0].id == first_id


def test_track_expires_after_ttl():
    reset_track_counter()
    tracker = CentroidTracker(ttl_seconds=3.0)
    tracker.update([(0.5, 0.5)], now=0.0)
    assert tracker.active_count() == 1

    # No detections for longer than the TTL -> the track is forgotten.
    tracker.update([], now=4.0)
    assert tracker.active_count() == 0


def test_returning_point_gets_new_id_no_reidentification():
    reset_track_counter()
    tracker = CentroidTracker(ttl_seconds=2.0)
    tracker.update([(0.5, 0.5)], now=0.0)
    original_id = tracker.tracks[0].id

    # Let the track expire completely.
    tracker.update([], now=5.0)
    assert tracker.active_count() == 0

    # The "same" location reappears: it must be a brand-new id (no memory).
    tracker.update([(0.5, 0.5)], now=6.0)
    assert tracker.tracks[0].id != original_id
    assert tracker.tracks[0].id > original_id


def test_created_total_counts_unique_tracks():
    reset_track_counter()
    tracker = CentroidTracker(ttl_seconds=1.0)
    tracker.update([(0.1, 0.1)], now=0.0)
    tracker.update([], now=2.0)  # expire
    tracker.update([(0.9, 0.9)], now=3.0)  # new track
    assert tracker.created_total == 2
