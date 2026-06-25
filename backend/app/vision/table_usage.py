"""Table-usage analytics — anonymous occupied/free state per table zone.

We track whether a *table area* currently contains anyone, how long it has been
in its current state, and how many times it has turned over. We never identify
who is sitting there. All metrics are about the *table*, not the guests.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.utils.geometry import Point
from app.vision.zones import Zone, ZoneType, zones_of_type


@dataclass
class TableState:
    """Mutable per-table state used to derive durations and turnover."""

    zone_id: str
    name: str
    occupied: bool = False
    state_since: float = 0.0
    turnover_count: int = 0
    _seats_history: list[float] = field(default_factory=list)

    def duration_seconds(self, now: float) -> int:
        return int(max(0.0, now - self.state_since))


@dataclass
class TableReading:
    """A per-table snapshot returned to the API/dashboard."""

    zone_id: str
    name: str
    occupied: bool
    duration_seconds: int
    turnover_count: int
    idle: bool

    def to_dict(self) -> dict:
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "occupied": self.occupied,
            "duration_seconds": self.duration_seconds,
            "turnover_count": self.turnover_count,
            "idle": self.idle,
        }


class TableUsageTracker:
    """Stateful tracker for table occupancy, dwell time, and turnover.

    Args:
        idle_threshold_seconds: A *free* table that stays empty for longer than
            this is flagged ``idle`` (unused capacity worth a manager's
            attention). Aggregate only.
    """

    def __init__(self, idle_threshold_seconds: float = 600.0) -> None:
        self.idle_threshold_seconds = idle_threshold_seconds
        self._tables: dict[str, TableState] = {}

    def _ensure_table(self, zone: Zone, now: float) -> TableState:
        state = self._tables.get(zone.id)
        if state is None:
            state = TableState(zone_id=zone.id, name=zone.name, state_since=now)
            self._tables[zone.id] = state
        return state

    def update(self, points: list[Point], zones: list[Zone], now: float) -> list[TableReading]:
        """Update table states from anonymous points and return readings."""
        readings: list[TableReading] = []
        for zone in zones_of_type(zones, ZoneType.TABLE):
            state = self._ensure_table(zone, now)
            is_occupied_now = any(zone.contains(p) for p in points)

            if is_occupied_now != state.occupied:
                # State transition: a free→occupied flip starts a new seating;
                # an occupied→free flip completes a turnover.
                if state.occupied and not is_occupied_now:
                    state.turnover_count += 1
                    state._seats_history.append(now - state.state_since)
                state.occupied = is_occupied_now
                state.state_since = now

            duration = state.duration_seconds(now)
            idle = (not state.occupied) and (duration >= self.idle_threshold_seconds)
            readings.append(
                TableReading(
                    zone_id=state.zone_id,
                    name=state.name,
                    occupied=state.occupied,
                    duration_seconds=duration,
                    turnover_count=state.turnover_count,
                    idle=idle,
                )
            )
        return readings

    def summary(self, now: float) -> dict:
        """Return aggregate table-usage statistics."""
        if not self._tables:
            return {"tables": 0, "occupied": 0, "free": 0, "occupancy_rate": 0.0,
                    "total_turnovers": 0, "avg_occupied_duration_seconds": 0}
        occupied = sum(1 for t in self._tables.values() if t.occupied)
        total = len(self._tables)
        durations = [d for t in self._tables.values() for d in t._seats_history]
        avg_dwell = int(sum(durations) / len(durations)) if durations else 0
        return {
            "tables": total,
            "occupied": occupied,
            "free": total - occupied,
            "occupancy_rate": round(occupied / total, 3),
            "total_turnovers": sum(t.turnover_count for t in self._tables.values()),
            "avg_occupied_duration_seconds": avg_dwell,
        }
