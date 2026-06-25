"""Aggregate analytics snapshot model.

Each row is an **anonymous, aggregate** reading: totals, per-zone counts, queue
pressure. The JSON ``payload`` holds the same aggregate structure returned by the
API. It contains **no** identities, tracks, bounding boxes, or imagery — only
numbers. Rows older than the retention window are pruned (see
:mod:`app.services.retention_service`).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.utils.time import utcnow


class AnalyticsSnapshotBase(SQLModel):
    camera_id: str
    total_occupancy: int = 0
    queue_count: int = 0
    queue_pressure: float = 0.0


class AnalyticsSnapshot(AnalyticsSnapshotBase, table=True):
    __tablename__ = "analytics_snapshots"

    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=utcnow, index=True)
    # Aggregate-only payload (occupancy.by_zone, queue, tables summary, ...).
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))


class AnalyticsSnapshotRead(AnalyticsSnapshotBase):
    id: int
    timestamp: datetime
    payload: dict
