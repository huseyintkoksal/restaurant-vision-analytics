"""Camera configuration model.

A camera record describes *where* analytics run — never any captured imagery.
Credentials (RTSP passwords, tokens) are **never** stored in the database; they
belong in environment variables or a secrets manager.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel

from app.utils.ids import new_resource_id
from app.utils.time import utcnow


class CameraStatus(StrEnum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class CameraBase(SQLModel):
    name: str
    location: str | None = None
    status: CameraStatus = CameraStatus.unknown
    # How frames are sourced. Never includes credentials.
    source_type: str = "demo"  # demo | rtsp | file | device


class Camera(CameraBase, table=True):
    __tablename__ = "cameras"

    id: str = Field(default_factory=lambda: new_resource_id("cam_"), primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    last_seen: datetime | None = None


class CameraCreate(CameraBase):
    """Input schema for creating a camera (no credentials accepted/stored)."""


class CameraRead(CameraBase):
    id: str
    created_at: datetime
    last_seen: datetime | None = None
