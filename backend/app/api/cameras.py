"""Camera configuration endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.session import get_session
from app.models.camera import CameraCreate, CameraRead
from app.services.camera_service import CameraService

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.get("", response_model=list[CameraRead])
def list_cameras(session: Session = Depends(get_session)) -> list:
    """List configured cameras (configuration only — no credentials)."""
    return CameraService(session).list_cameras()


@router.post("", response_model=CameraRead, status_code=201)
def create_camera(
    payload: CameraCreate, session: Session = Depends(get_session)
):
    """Create a camera configuration. Credentials are never accepted or stored."""
    return CameraService(session).create_camera(payload)


@router.get("/{camera_id}", response_model=CameraRead)
def get_camera(camera_id: str, session: Session = Depends(get_session)):
    """Fetch a single camera by id."""
    camera = CameraService(session).get_camera(camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera
