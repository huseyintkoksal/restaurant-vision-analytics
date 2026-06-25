"""Database engine and session lifecycle.

Defaults to local-first SQLite. The engine is created lazily so tests can point
``DATABASE_URL`` at an in-memory or temp database before anything connects.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

_engine: Engine | None = None


def _ensure_sqlite_dir(database_url: str) -> None:
    """Create the parent directory for a file-based SQLite database."""
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return
    raw_path = database_url[len(prefix) :]
    if not raw_path or raw_path == ":memory:":
        return
    path = Path(raw_path)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def get_engine() -> Engine:
    """Return the process-wide SQLModel engine, creating it on first use."""
    global _engine
    if _engine is None:
        settings = get_settings()
        database_url = os.environ.get("DATABASE_URL", settings.database_url)
        _ensure_sqlite_dir(database_url)
        connect_args = (
            {"check_same_thread": False} if database_url.startswith("sqlite") else {}
        )
        _engine = create_engine(database_url, echo=False, connect_args=connect_args)
    return _engine


def init_engine_for_tests(database_url: str) -> Engine:
    """Reset and rebuild the engine against ``database_url`` (test helper)."""
    global _engine
    _ensure_sqlite_dir(database_url)
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    _engine = create_engine(database_url, echo=False, connect_args=connect_args)
    return _engine


def create_db_and_tables() -> None:
    """Create all tables defined on the SQLModel metadata."""
    # Importing the models registers them on SQLModel.metadata.
    from app import models  # noqa: F401

    SQLModel.metadata.create_all(get_engine())


def get_session() -> Iterator[Session]:
    """FastAPI dependency yielding a database session."""
    with Session(get_engine()) as session:
        yield session
