"""Zone configuration endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.repositories import ZoneRepository
from app.database.session import get_session
from app.models.zone import ZoneCreate, ZoneRead, ZoneRecord

router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("", response_model=list[ZoneRead])
def list_zones(
    camera_id: str | None = None, session: Session = Depends(get_session)
) -> list:
    """List configured zones, optionally filtered by camera."""
    return ZoneRepository(session).list(camera_id=camera_id)


@router.post("", response_model=ZoneRead, status_code=201)
def create_zone(payload: ZoneCreate, session: Session = Depends(get_session)):
    """Create a zone (a named polygon). Zones describe places, not people."""
    zone = ZoneRecord(
        name=payload.name,
        type=payload.type,
        camera_id=payload.camera_id,
        capacity=payload.capacity,
        polygon=payload.polygon,
        attributes=payload.attributes,
    )
    return ZoneRepository(session).create(zone)
