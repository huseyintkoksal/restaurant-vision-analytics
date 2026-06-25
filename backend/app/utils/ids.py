"""Identifier helpers.

Track identifiers produced here are **ephemeral and anonymous**. They exist
only to associate detections across a handful of consecutive frames so that
counts and dwell times can be computed. They are:

* never derived from appearance, biometrics, or any personal attribute;
* never persisted to the database;
* recycled/forgotten once a track expires (see :mod:`app.vision.tracker`).
"""

from __future__ import annotations

import itertools
import uuid

# Monotonic counter for short-lived, in-memory track ids. Resets per process.
_track_counter = itertools.count(1)


def next_track_id() -> int:
    """Return the next ephemeral, in-memory track id (anonymous integer)."""
    return next(_track_counter)


def new_resource_id(prefix: str = "") -> str:
    """Return a random opaque id for non-personal resources (cameras, zones).

    These identify *configuration objects*, not people.
    """
    token = uuid.uuid4().hex[:12]
    return f"{prefix}{token}" if prefix else token


def reset_track_counter() -> None:
    """Reset the ephemeral track counter (used in tests)."""
    global _track_counter
    _track_counter = itertools.count(1)
