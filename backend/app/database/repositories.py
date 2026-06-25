"""Thin repository helpers over SQLModel sessions.

Repositories isolate query logic from the API layer. They handle only
configuration objects (cameras, zones) and aggregate analytics (snapshots,
alerts) — never personal data.
"""

from __future__ import annotations

from datetime import datetime

from sqlmodel import Session, select

from app.models.alert import Alert
from app.models.analytics_snapshot import AnalyticsSnapshot
from app.models.camera import Camera
from app.models.zone import ZoneRecord


# --- Cameras ---------------------------------------------------------------
class CameraRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Camera]:
        return list(self.session.exec(select(Camera)).all())

    def get(self, camera_id: str) -> Camera | None:
        return self.session.get(Camera, camera_id)

    def create(self, camera: Camera) -> Camera:
        self.session.add(camera)
        self.session.commit()
        self.session.refresh(camera)
        return camera


# --- Zones -----------------------------------------------------------------
class ZoneRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, camera_id: str | None = None) -> list[ZoneRecord]:
        statement = select(ZoneRecord)
        if camera_id:
            statement = statement.where(ZoneRecord.camera_id == camera_id)
        return list(self.session.exec(statement).all())

    def get(self, zone_id: str) -> ZoneRecord | None:
        return self.session.get(ZoneRecord, zone_id)

    def create(self, zone: ZoneRecord) -> ZoneRecord:
        self.session.add(zone)
        self.session.commit()
        self.session.refresh(zone)
        return zone


# --- Analytics snapshots ---------------------------------------------------
class SnapshotRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, snapshot: AnalyticsSnapshot) -> AnalyticsSnapshot:
        self.session.add(snapshot)
        self.session.commit()
        self.session.refresh(snapshot)
        return snapshot

    def recent(self, limit: int = 100) -> list[AnalyticsSnapshot]:
        statement = (
            select(AnalyticsSnapshot)
            .order_by(AnalyticsSnapshot.timestamp.desc())  # type: ignore[attr-defined]
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def delete_older_than(self, cutoff: datetime) -> int:
        statement = select(AnalyticsSnapshot).where(AnalyticsSnapshot.timestamp < cutoff)
        rows = list(self.session.exec(statement).all())
        for row in rows:
            self.session.delete(row)
        self.session.commit()
        return len(rows)


# --- Alerts ----------------------------------------------------------------
class AlertRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, limit: int = 100, unresolved_only: bool = False) -> list[Alert]:
        statement = select(Alert)
        if unresolved_only:
            statement = statement.where(Alert.resolved == False)  # noqa: E712
        statement = statement.order_by(Alert.created_at.desc()).limit(limit)  # type: ignore[attr-defined]
        return list(self.session.exec(statement).all())

    def add(self, alert: Alert) -> Alert:
        self.session.add(alert)
        self.session.commit()
        self.session.refresh(alert)
        return alert

    def delete_older_than(self, cutoff: datetime) -> int:
        statement = select(Alert).where(Alert.created_at < cutoff)
        rows = list(self.session.exec(statement).all())
        for row in rows:
            self.session.delete(row)
        self.session.commit()
        return len(rows)
