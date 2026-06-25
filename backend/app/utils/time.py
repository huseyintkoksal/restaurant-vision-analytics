"""Time helpers — all timestamps are timezone-aware UTC."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(UTC)


def iso(dt: datetime | None = None) -> str:
    """Return an ISO-8601 string (``...Z``) for ``dt`` (default: now)."""
    dt = dt or utcnow()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def cutoff_for_retention(retention_days: int, now: datetime | None = None) -> datetime:
    """Return the timestamp before which data should be pruned.

    Args:
        retention_days: How many days of data to keep. ``<= 0`` disables
            pruning and returns the Unix epoch (effectively "keep nothing older
            than the beginning of time" → prune nothing).
    """
    now = now or utcnow()
    if retention_days <= 0:
        return datetime.fromtimestamp(0, tz=UTC)
    return now - timedelta(days=retention_days)


def seconds_between(start: datetime, end: datetime | None = None) -> float:
    """Return the number of seconds between ``start`` and ``end`` (default now)."""
    end = end or utcnow()
    return (end - start).total_seconds()
