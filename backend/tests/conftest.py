"""Pytest fixtures.

Configures an isolated, temporary SQLite database **before** importing any app
module, so tests never touch a developer's real data.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

# --- Environment must be set before importing app modules -------------------
_TMP_DIR = tempfile.mkdtemp(prefix="rva-test-")
_DB_PATH = Path(_TMP_DIR) / "test.db"

os.environ["APP_ENV"] = "test"
os.environ["ENABLE_DEMO_MODE"] = "true"
os.environ["ENABLE_RAW_FRAME_STORAGE"] = "false"
os.environ["DATA_RETENTION_DAYS"] = "7"
os.environ["LIVE_UPDATE_INTERVAL_SECONDS"] = "2"
os.environ["DATABASE_URL"] = "sqlite:///" + str(_DB_PATH).replace("\\", "/")

from app.config import get_settings  # noqa: E402

get_settings.cache_clear()

from app.database.init_db import init_db  # noqa: E402
from app.database.session import init_engine_for_tests  # noqa: E402
from app.services.analytics_service import reset_analytics_service  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _database():
    init_engine_for_tests(os.environ["DATABASE_URL"])
    init_db(seed=True)
    reset_analytics_service()
    yield


@pytest.fixture
def client():
    """A FastAPI TestClient with the app lifespan active."""
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
