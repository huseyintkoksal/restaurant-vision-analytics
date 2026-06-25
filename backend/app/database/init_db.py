"""Database initialization and demo seeding.

On startup we create the tables and, in demo mode, seed a single demo camera and
a generic restaurant floor plan (entrance, queue, cashier, dining area, tables).
All seeded data is configuration — no personal data is ever seeded.
"""

from __future__ import annotations

from sqlmodel import Session, select

from app.database.session import create_db_and_tables, get_engine
from app.models.camera import Camera, CameraStatus
from app.models.zone import ZoneRecord
from app.vision.zones import ZoneType

DEMO_CAMERA_ID = "demo-camera-1"


def _rect(cx: float, cy: float, hw: float, hh: float) -> list[list[float]]:
    """Axis-aligned rectangle polygon centered at ``(cx, cy)``."""
    return [
        [round(cx - hw, 3), round(cy - hh, 3)],
        [round(cx + hw, 3), round(cy - hh, 3)],
        [round(cx + hw, 3), round(cy + hh, 3)],
        [round(cx - hw, 3), round(cy + hh, 3)],
    ]


def default_demo_zones(camera_id: str = DEMO_CAMERA_ID) -> list[ZoneRecord]:
    """Return a generic restaurant floor plan matching the synthetic detector."""
    table_anchors = [
        (0.62, 0.30),
        (0.78, 0.30),
        (0.62, 0.52),
        (0.78, 0.52),
        (0.62, 0.74),
        (0.78, 0.74),
    ]
    zones: list[ZoneRecord] = [
        ZoneRecord(
            id="entrance-1", name="Entrance", type=ZoneType.ENTRANCE,
            camera_id=camera_id, polygon=_rect(0.10, 0.88, 0.10, 0.10),
        ),
        ZoneRecord(
            id="queue-1", name="Order Queue", type=ZoneType.QUEUE, capacity=6,
            camera_id=camera_id, polygon=_rect(0.30, 0.62, 0.12, 0.12),
        ),
        ZoneRecord(
            id="cashier-1", name="Cashier", type=ZoneType.CASHIER,
            camera_id=camera_id, polygon=_rect(0.46, 0.50, 0.07, 0.08),
        ),
        ZoneRecord(
            id="dining-1", name="Dining Area", type=ZoneType.DINING_AREA, capacity=12,
            camera_id=camera_id, polygon=_rect(0.73, 0.52, 0.19, 0.34),
        ),
    ]
    for i, (cx, cy) in enumerate(table_anchors, start=1):
        zones.append(
            ZoneRecord(
                id=f"table-{i}", name=f"Table {i}", type=ZoneType.TABLE, capacity=4,
                camera_id=camera_id, polygon=_rect(cx, cy, 0.07, 0.11),
                attributes={"seats": 4},
            )
        )
    return zones


def seed_demo_data(session: Session) -> None:
    """Seed the demo camera and zones if the database is empty."""
    existing = session.exec(select(Camera)).first()
    if existing is not None:
        return

    camera = Camera(
        id=DEMO_CAMERA_ID,
        name="Demo Camera",
        location="Front of house",
        status=CameraStatus.online,
        source_type="demo",
    )
    session.add(camera)
    for zone in default_demo_zones():
        session.add(zone)
    session.commit()


def init_db(seed: bool = True) -> None:
    """Create tables and optionally seed demo data."""
    create_db_and_tables()
    if seed:
        with Session(get_engine()) as session:
            seed_demo_data(session)
