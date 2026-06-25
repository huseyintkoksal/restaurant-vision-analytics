"""Analytics endpoints — aggregate, anonymous metrics only."""

from __future__ import annotations

from fastapi import APIRouter

from app.services.analytics_service import get_analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/live")
def live() -> dict:
    """Return the latest live aggregate snapshot (occupancy, queue, tables)."""
    return get_analytics_service().get_engine().live()


@router.get("/summary")
def summary() -> dict:
    """Return session aggregates: peak/average occupancy, visitors, peak hour."""
    return get_analytics_service().get_engine().summary()


@router.get("/heatmap")
def heatmap() -> dict:
    """Return the anonymous spatial density grid (crowd hotspots, not people)."""
    return get_analytics_service().get_engine().heatmap_data()


@router.get("/tables")
def tables() -> dict:
    """Return per-table occupied/free state, dwell time, and turnover."""
    return get_analytics_service().get_engine().tables_data()


@router.get("/queue")
def queue() -> dict:
    """Return current queue count, pressure score, and status."""
    return get_analytics_service().get_engine().queue_data()


@router.get("/history")
def history() -> dict:
    """Return the recent occupancy/queue time series for charts."""
    return {"series": get_analytics_service().get_engine().history()}
