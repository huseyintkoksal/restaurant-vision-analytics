"""Operational alert endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database.repositories import AlertRepository
from app.database.session import get_session
from app.models.alert import AlertRead

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(
    limit: int = Query(50, ge=1, le=500),
    unresolved_only: bool = False,
    session: Session = Depends(get_session),
) -> list:
    """List recent operational alerts (queue, occupancy, table idle, camera)."""
    return AlertRepository(session).list(limit=limit, unresolved_only=unresolved_only)
