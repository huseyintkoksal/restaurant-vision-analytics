"""Operational alert model.

Alerts are operational signals (a queue is long, a table sat empty, a camera went
offline, occupancy crossed a threshold). They are about *places and aggregate
conditions*, never about a specific person.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel

from app.utils.time import utcnow


class AlertType(StrEnum):
    queue_too_long = "queue_too_long"
    table_idle = "table_idle"
    camera_offline = "camera_offline"
    occupancy_threshold = "occupancy_threshold"


class AlertSeverity(StrEnum):
    info = "info"
    warning = "warning"
    critical = "critical"


class AlertBase(SQLModel):
    type: AlertType
    severity: AlertSeverity = AlertSeverity.warning
    message: str
    camera_id: str | None = None
    zone_id: str | None = None
    value: float | None = None


class Alert(AlertBase, table=True):
    __tablename__ = "alerts"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow, index=True)
    resolved: bool = False


class AlertRead(AlertBase):
    id: int
    created_at: datetime
    resolved: bool
