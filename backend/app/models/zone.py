"""Zone configuration model.

A zone is a named polygon over a camera view. It is configuration — it describes
*places*, not people. The ``ZoneType`` enum is shared with the runtime vision
layer so there is a single source of truth.
"""

from __future__ import annotations

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.utils.ids import new_resource_id
from app.vision.zones import Zone as RuntimeZone
from app.vision.zones import ZoneType


class ZoneBase(SQLModel):
    name: str
    type: ZoneType
    camera_id: str | None = None
    capacity: int | None = None


class ZoneRecord(ZoneBase, table=True):
    __tablename__ = "zones"

    id: str = Field(default_factory=lambda: new_resource_id("zone_"), primary_key=True)
    # Ordered [[x, y], ...] vertices in normalized (0–1) coordinates.
    polygon: list = Field(default_factory=list, sa_column=Column(JSON))
    # Non-personal configuration only (e.g. {"seats": 4}). Named "attributes"
    # rather than "metadata" because SQLAlchemy reserves the latter.
    attributes: dict = Field(default_factory=dict, sa_column=Column(JSON))

    def to_runtime(self) -> RuntimeZone:
        """Convert to the dependency-light runtime :class:`Zone`."""
        return RuntimeZone(
            id=self.id,
            name=self.name,
            type=self.type,
            polygon=[tuple(p) for p in self.polygon],
            capacity=self.capacity,
            metadata=dict(self.attributes or {}),
        )


class ZoneCreate(ZoneBase):
    polygon: list = Field(default_factory=list)
    attributes: dict = Field(default_factory=dict)


class ZoneRead(ZoneBase):
    id: str
    polygon: list
    attributes: dict
