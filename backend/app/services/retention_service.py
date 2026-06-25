"""Data-retention service.

Enforces the configured retention window by pruning aggregate snapshots and
alerts older than the cutoff. This is a core privacy control: by default we keep
only a short rolling window of **anonymous, aggregate** metrics.
"""

from __future__ import annotations

from sqlmodel import Session

from app.database.repositories import AlertRepository, SnapshotRepository
from app.utils.time import cutoff_for_retention


class RetentionService:
    """Prunes data older than ``retention_days``."""

    def __init__(self, retention_days: int = 7) -> None:
        self.retention_days = retention_days

    def prune(self, session: Session) -> dict[str, int]:
        """Delete snapshots and alerts older than the retention window.

        Returns a count of deleted rows per table.
        """
        cutoff = cutoff_for_retention(self.retention_days)
        snapshots_deleted = SnapshotRepository(session).delete_older_than(cutoff)
        alerts_deleted = AlertRepository(session).delete_older_than(cutoff)
        return {
            "snapshots_deleted": snapshots_deleted,
            "alerts_deleted": alerts_deleted,
            "cutoff": cutoff.isoformat(),
        }
