"""Health and meta endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app import __version__
from app.config import get_settings
from app.models.privacy import PRIVACY_STATEMENT
from app.utils.time import iso

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness probe with privacy posture and demo-mode status."""
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "app_env": settings.app_env,
        "demo_mode": settings.enable_demo_mode,
        "time": iso(),
        "privacy": settings.privacy_summary,
        "privacy_statement": PRIVACY_STATEMENT,
    }
