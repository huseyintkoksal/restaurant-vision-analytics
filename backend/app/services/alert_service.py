"""Alert evaluation.

Turns aggregate analytics into operational alerts. The evaluator is
*edge-triggered* and de-duplicated: an alert fires once when a condition becomes
true and will not re-fire until the condition clears, so the alert feed stays
useful instead of noisy.

All alerts describe places and aggregate conditions — never a person.
"""

from __future__ import annotations

from app.models.alert import Alert, AlertSeverity, AlertType


class AlertEvaluator:
    """Stateful, de-duplicated alert evaluator.

    Args:
        queue_threshold: Queue pressure (0–1) above which a queue alert fires.
        occupancy_threshold: Total occupancy above which an occupancy alert fires.
    """

    def __init__(self, queue_threshold: float = 0.8, occupancy_threshold: int = 25) -> None:
        self.queue_threshold = queue_threshold
        self.occupancy_threshold = occupancy_threshold
        self._active: set[str] = set()

    def evaluate(self, snapshot: dict) -> list[Alert]:
        """Return newly-triggered alerts for a live snapshot."""
        camera_id = snapshot.get("camera_id")
        new_alerts: list[Alert] = []

        # --- Queue too long ---
        queue = snapshot.get("queue", {})
        q_pressure = float(queue.get("pressure_score", 0.0))
        new_alerts += self._edge(
            key=f"queue:{camera_id}",
            condition=q_pressure >= self.queue_threshold,
            build=lambda: Alert(
                type=AlertType.queue_too_long,
                severity=AlertSeverity.warning,
                message=f"Queue pressure high ({q_pressure:.0%}). Consider opening another till.",
                camera_id=camera_id,
                value=q_pressure,
            ),
        )

        # --- Occupancy threshold ---
        total = int(snapshot.get("occupancy", {}).get("total", 0))
        new_alerts += self._edge(
            key=f"occupancy:{camera_id}",
            condition=total >= self.occupancy_threshold,
            build=lambda: Alert(
                type=AlertType.occupancy_threshold,
                severity=AlertSeverity.warning,
                message=f"Occupancy reached {total} (threshold {self.occupancy_threshold}).",
                camera_id=camera_id,
                value=float(total),
            ),
        )

        # --- Table idle too long ---
        for table in snapshot.get("tables", []):
            zone_id = table.get("zone_id")
            new_alerts += self._edge(
                key=f"table_idle:{zone_id}",
                condition=bool(table.get("idle")),
                build=lambda t=table: Alert(
                    type=AlertType.table_idle,
                    severity=AlertSeverity.info,
                    message=f"{t.get('name', 'Table')} idle for "
                    f"{int(t.get('duration_seconds', 0)) // 60} min.",
                    camera_id=camera_id,
                    zone_id=t.get("zone_id"),
                    value=float(t.get("duration_seconds", 0)),
                ),
            )

        return new_alerts

    def camera_offline(self, camera_id: str) -> list[Alert]:
        """Emit a camera-offline alert (edge-triggered)."""
        return self._edge(
            key=f"camera_offline:{camera_id}",
            condition=True,
            build=lambda: Alert(
                type=AlertType.camera_offline,
                severity=AlertSeverity.critical,
                message=f"Camera {camera_id} is offline.",
                camera_id=camera_id,
            ),
        )

    def camera_online(self, camera_id: str) -> None:
        """Clear the offline state so a future outage can alert again."""
        self._active.discard(f"camera_offline:{camera_id}")

    def _edge(self, key: str, condition: bool, build) -> list[Alert]:
        """Fire ``build()`` once on a rising edge; clear state on falling edge."""
        if condition:
            if key in self._active:
                return []
            self._active.add(key)
            return [build()]
        self._active.discard(key)
        return []
