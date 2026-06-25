"""Ephemeral centroid tracker.

This tracker associates detections across consecutive frames *only* to compute
short-term metrics such as dwell time and movement direction. Its design is
privacy-preserving by construction:

* Track ids are anonymous integers with no link to appearance or identity.
* There is **no re-identification**: a person who leaves and returns receives a
  brand-new id. We never "recognise" anyone.
* Tracks live for at most ``ttl_seconds`` without a fresh detection, then are
  permanently forgotten.
* Nothing here is persisted to the database.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.utils.geometry import Point, euclidean_distance
from app.utils.ids import next_track_id


@dataclass
class Track:
    """A short-lived, anonymous association of detections across frames."""

    id: int
    centroid: Point
    created_at: float
    last_seen: float
    hits: int = 1
    # A short trail of recent positions (bounded) for direction/heatmap use.
    trail: list[Point] = field(default_factory=list)

    def age(self, now: float) -> float:
        return now - self.created_at

    def staleness(self, now: float) -> float:
        return now - self.last_seen


class CentroidTracker:
    """Greedy nearest-centroid tracker with a time-to-live.

    Args:
        ttl_seconds: Maximum time a track may survive without a new detection.
        max_match_distance: Maximum normalized distance for a detection to be
            associated with an existing track.
        trail_length: How many recent points to retain per track.
    """

    def __init__(
        self,
        ttl_seconds: float = 5.0,
        max_match_distance: float = 0.15,
        trail_length: int = 16,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_match_distance = max_match_distance
        self.trail_length = trail_length
        self._tracks: dict[int, Track] = {}
        # Aggregate count of tracks ever created this session. This is a plain
        # integer (a count, not an identity log) used to estimate visitor flow.
        self.created_total = 0

    @property
    def tracks(self) -> list[Track]:
        """Return the currently active (non-expired) tracks."""
        return list(self._tracks.values())

    def active_count(self) -> int:
        return len(self._tracks)

    def update(self, points: list[Point], now: float) -> list[Track]:
        """Associate ``points`` with existing tracks and expire stale ones.

        Returns the list of active tracks after the update.
        """
        self._expire(now)

        unmatched_points = set(range(len(points)))
        # Greedy matching: for each existing track, take the closest free point.
        for track in sorted(self._tracks.values(), key=lambda t: t.last_seen):
            best_idx: int | None = None
            best_dist = self.max_match_distance
            for idx in unmatched_points:
                dist = euclidean_distance(track.centroid, points[idx])
                if dist <= best_dist:
                    best_dist = dist
                    best_idx = idx
            if best_idx is not None:
                self._update_track(track, points[best_idx], now)
                unmatched_points.discard(best_idx)

        # Remaining points become brand-new tracks (no re-identification).
        for idx in unmatched_points:
            self._create_track(points[idx], now)

        return self.tracks

    def _expire(self, now: float) -> None:
        expired = [
            tid for tid, t in self._tracks.items() if t.staleness(now) > self.ttl_seconds
        ]
        for tid in expired:
            # Forget completely — no archival, no re-identification record.
            del self._tracks[tid]

    def _create_track(self, point: Point, now: float) -> Track:
        track = Track(
            id=next_track_id(),
            centroid=point,
            created_at=now,
            last_seen=now,
            trail=[point],
        )
        self._tracks[track.id] = track
        self.created_total += 1
        return track

    def _update_track(self, track: Track, point: Point, now: float) -> None:
        track.centroid = point
        track.last_seen = now
        track.hits += 1
        track.trail.append(point)
        if len(track.trail) > self.trail_length:
            track.trail = track.trail[-self.trail_length :]

    def reset(self) -> None:
        """Forget all tracks (e.g. on camera change)."""
        self._tracks.clear()
