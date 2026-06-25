"""Synthetic detector for demo mode and tests.

:class:`SyntheticDetector` simulates anonymous customer flow through a restaurant
without any camera. It models a handful of anonymous "agents" that arrive,
queue, sit at tables, and leave — producing realistic, time-varying occupancy,
queue, and table-usage signals for the dashboard.

It is the default, fully deterministic-with-a-seed detector. No imagery, no
identities, no personal attributes — just moving points.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from app.utils.geometry import Point, euclidean_distance
from app.vision.detector_base import Detection, Detector, DetectorInfo

# Canonical anchor points (normalized) used to lay out a generic restaurant.
_ENTRANCE: Point = (0.10, 0.88)
_QUEUE: Point = (0.30, 0.62)
_CASHIER: Point = (0.46, 0.50)
_TABLES: list[Point] = [
    (0.62, 0.30),
    (0.78, 0.30),
    (0.62, 0.52),
    (0.78, 0.52),
    (0.62, 0.74),
    (0.78, 0.74),
]

# Agent lifecycle phases.
_ARRIVE = "arrive"
_QUEUE_WAIT = "queue"
_SEAT = "seat"
_DINE = "dine"
_LEAVE = "leave"


@dataclass
class _Agent:
    x: float
    y: float
    phase: str
    target: Point
    phase_end: float
    table_idx: int | None = None
    speed: float = 0.05

    @property
    def point(self) -> Point:
        return (self.x, self.y)


class SyntheticDetector(Detector):
    """Camera-free detector that simulates anonymous customer flow.

    Args:
        seed: RNG seed for reproducible demos/tests.
        step_seconds: How much simulated time passes per :meth:`detect` call.
        base_arrival_rate: Expected arrivals per simulated minute at baseline.
        max_agents: Hard cap on concurrent anonymous agents.
    """

    def __init__(
        self,
        seed: int | None = 7,
        step_seconds: float = 2.0,
        base_arrival_rate: float = 14.0,
        max_agents: int = 40,
    ) -> None:
        self._rng = random.Random(seed)
        self.step_seconds = step_seconds
        self.base_arrival_rate = base_arrival_rate
        self.max_agents = max_agents
        self._agents: list[_Agent] = []
        self._table_taken: dict[int, bool] = {i: False for i in range(len(_TABLES))}
        self._t = 0.0

    @property
    def info(self) -> DetectorInfo:
        return DetectorInfo(
            name="SyntheticDetector",
            requires_model_download=False,
            notes="Camera-free simulation of anonymous customer flow for demos and tests.",
        )

    # -- public API -------------------------------------------------------
    def detect(self, frame=None) -> list[Detection]:  # noqa: ARG002 - frame unused
        """Advance the simulation by ``step_seconds`` and return detections."""
        self._t += self.step_seconds
        self._maybe_spawn()
        self._advance_agents()
        return [self._as_detection(agent) for agent in self._agents]

    # -- simulation internals --------------------------------------------
    def _busyness(self) -> float:
        """A smooth 0.3–1.0 multiplier emulating quiet/busy cycles."""
        return 0.65 + 0.35 * math.sin(self._t / 120.0)

    def _maybe_spawn(self) -> None:
        if len(self._agents) >= self.max_agents:
            return
        arrivals_per_second = (self.base_arrival_rate * self._busyness()) / 60.0
        expected = arrivals_per_second * self.step_seconds
        # Poisson-ish: spawn an integer number of arrivals this step.
        count = self._poisson(expected)
        for _ in range(count):
            if len(self._agents) >= self.max_agents:
                break
            self._spawn_agent()

    def _poisson(self, lam: float) -> int:
        # Knuth's algorithm — adequate for small lambda.
        if lam <= 0:
            return 0
        target = math.exp(-lam)
        k = 0
        product = 1.0
        while True:
            k += 1
            product *= self._rng.random()
            if product <= target:
                return k - 1

    def _spawn_agent(self) -> None:
        jitter = lambda v, s=0.02: v + self._rng.uniform(-s, s)  # noqa: E731
        agent = _Agent(
            x=jitter(_ENTRANCE[0]),
            y=jitter(_ENTRANCE[1]),
            phase=_ARRIVE,
            target=(jitter(_QUEUE[0]), jitter(_QUEUE[1])),
            phase_end=self._t + self._rng.uniform(4, 10),
            speed=self._rng.uniform(0.035, 0.06),
        )
        self._agents.append(agent)

    def _advance_agents(self) -> None:
        survivors: list[_Agent] = []
        for agent in self._agents:
            self._move_toward(agent)
            self._maybe_transition(agent)
            if agent.phase == "done":
                if agent.table_idx is not None:
                    self._table_taken[agent.table_idx] = False
                continue
            survivors.append(agent)
        self._agents = survivors

    def _move_toward(self, agent: _Agent) -> None:
        if agent.phase in (_QUEUE_WAIT, _DINE):
            # Small idle wandering while waiting/sitting.
            agent.x += self._rng.uniform(-0.004, 0.004)
            agent.y += self._rng.uniform(-0.004, 0.004)
            return
        tx, ty = agent.target
        dist = euclidean_distance(agent.point, agent.target)
        if dist < 1e-6:
            return
        move = min(agent.speed * self.step_seconds, dist)
        agent.x += (tx - agent.x) / dist * move
        agent.y += (ty - agent.y) / dist * move

    def _maybe_transition(self, agent: _Agent) -> None:
        arrived = euclidean_distance(agent.point, agent.target) < 0.03
        if agent.phase == _ARRIVE and arrived:
            agent.phase = _QUEUE_WAIT
            agent.phase_end = self._t + self._rng.uniform(6, 20)
        elif agent.phase == _QUEUE_WAIT and self._t >= agent.phase_end:
            table_idx = self._claim_table()
            if table_idx is None:
                # No free table; keep waiting a bit longer.
                agent.phase_end = self._t + self._rng.uniform(4, 8)
            else:
                agent.phase = _SEAT
                agent.table_idx = table_idx
                agent.target = _TABLES[table_idx]
        elif agent.phase == _SEAT and arrived:
            agent.phase = _DINE
            agent.phase_end = self._t + self._rng.uniform(40, 160)
        elif agent.phase == _DINE and self._t >= agent.phase_end:
            agent.phase = _LEAVE
            if agent.table_idx is not None:
                self._table_taken[agent.table_idx] = False
                agent.table_idx = None
            agent.target = _ENTRANCE
        elif agent.phase == _LEAVE and arrived:
            agent.phase = "done"

    def _claim_table(self) -> int | None:
        free = [i for i, taken in self._table_taken.items() if not taken]
        if not free:
            return None
        idx = self._rng.choice(free)
        self._table_taken[idx] = True
        return idx

    def _as_detection(self, agent: _Agent) -> Detection:
        # Build an anonymous person-shaped box whose foot point is the agent.
        x = min(max(agent.x, 0.02), 0.98)
        y = min(max(agent.y, 0.12), 0.98)
        bbox = (x - 0.02, y - 0.12, x + 0.02, y)
        return Detection(bbox=bbox, confidence=0.9, label="person")


# Backwards/intuitive alias — both names refer to the same camera-free detector.
MockDetector = SyntheticDetector
