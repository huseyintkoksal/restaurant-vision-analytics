"""Camera service — configuration-only camera management.

This service manages camera *configuration*. It never handles, stores, or logs
camera credentials; connection secrets must come from environment variables or a
secrets manager at runtime.
"""

from __future__ import annotations

from sqlmodel import Session

from app.database.repositories import CameraRepository
from app.models.camera import Camera, CameraCreate
from app.utils.time import utcnow


class CameraService:
    def __init__(self, session: Session) -> None:
        self.repo = CameraRepository(session)

    def list_cameras(self) -> list[Camera]:
        return self.repo.list()

    def get_camera(self, camera_id: str) -> Camera | None:
        return self.repo.get(camera_id)

    def create_camera(self, data: CameraCreate) -> Camera:
        camera = Camera(**data.model_dump())
        return self.repo.create(camera)

    def mark_seen(self, camera_id: str) -> Camera | None:
        camera = self.repo.get(camera_id)
        if camera is None:
            return None
        camera.last_seen = utcnow()
        self.repo.session.add(camera)
        self.repo.session.commit()
        self.repo.session.refresh(camera)
        return camera
