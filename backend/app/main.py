"""FastAPI application entrypoint.

Wires the routers, CORS, database initialization, and the demo analytics loop.
Privacy defaults are applied here and surfaced through ``/health`` and
``/api/privacy``.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import alerts, analytics, cameras, health, websocket, zones
from app.config import get_settings
from app.database.init_db import init_db
from app.models.privacy import PrivacyStatus
from app.services.analytics_service import get_analytics_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rva")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    # Seed demo data only when demo mode is on.
    init_db(seed=settings.enable_demo_mode)
    service = get_analytics_service()
    service.configure()
    await service.start_demo_loop()
    logger.info(
        "%s v%s started (demo_mode=%s)",
        settings.app_name,
        __version__,
        settings.enable_demo_mode,
    )
    try:
        yield
    finally:
        await service.stop()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "Privacy-first computer vision toolkit for restaurant occupancy, queue, "
            "table usage and customer flow analytics. No facial recognition, no "
            "biometrics, no persistent customer tracking."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(cameras.router)
    app.include_router(zones.router)
    app.include_router(analytics.router)
    app.include_router(alerts.router)
    app.include_router(websocket.router)

    @app.get("/", tags=["meta"])
    def root() -> dict:
        return {
            "name": settings.app_name,
            "version": __version__,
            "docs": "/docs",
            "privacy": "/api/privacy",
        }

    @app.get("/api/privacy", response_model=PrivacyStatus, tags=["privacy"])
    def privacy() -> PrivacyStatus:
        return PrivacyStatus(
            raw_frame_storage=settings.enable_raw_frame_storage,
            data_retention_days=settings.data_retention_days,
        )

    return app


app = create_app()
