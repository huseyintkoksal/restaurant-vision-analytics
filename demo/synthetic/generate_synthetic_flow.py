#!/usr/bin/env python
"""Generate a synthetic, anonymous customer-flow event file.

This script drives the same :class:`SyntheticDetector` used by demo mode and
writes a JSON timeline of **aggregate, anonymous** snapshots (occupancy, queue,
tables). No imagery, identities, or personal attributes are produced — there is
nothing personal to produce.

Usage:
    python demo/synthetic/generate_synthetic_flow.py --frames 120 \
        --out demo/synthetic/sample_events.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make the backend package importable when run from the repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.database.init_db import default_demo_zones  # noqa: E402
from app.vision.analytics_engine import AnalyticsEngine  # noqa: E402
from app.vision.mock_detector import SyntheticDetector  # noqa: E402


def generate_events(frames: int = 120, seed: int = 7, arrival_rate: float = 30.0) -> list[dict]:
    """Run the synthetic pipeline for ``frames`` ticks and return snapshots."""
    zones = [z.to_runtime() for z in default_demo_zones()]
    engine = AnalyticsEngine(
        detector=SyntheticDetector(seed=seed, base_arrival_rate=arrival_rate),
        zones=zones,
    )
    events: list[dict] = []
    for _ in range(frames):
        snap = engine.tick()
        events.append(
            {
                "timestamp": snap["timestamp"],
                "occupancy_total": snap["occupancy"]["total"],
                "occupancy_by_type": snap["occupancy"].get("by_type", {}),
                "queue": snap["queue"],
                "tables_occupied": sum(1 for t in snap["tables"] if t["occupied"]),
                "tables_total": len(snap["tables"]),
            }
        )
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=120, help="number of snapshots")
    parser.add_argument("--seed", type=int, default=7, help="RNG seed for reproducibility")
    parser.add_argument("--arrival-rate", type=float, default=30.0, help="arrivals per minute")
    parser.add_argument(
        "--out",
        type=str,
        default=str(Path(__file__).with_name("sample_events.json")),
        help="output JSON path",
    )
    args = parser.parse_args()

    events = generate_events(frames=args.frames, seed=args.seed, arrival_rate=args.arrival_rate)
    summary = {
        "description": "Synthetic, anonymous restaurant flow generated for demos. No imagery, "
        "identities, or personal attributes.",
        "frames": len(events),
        "peak_occupancy": max((e["occupancy_total"] for e in events), default=0),
        "events": events,
    }
    out_path = Path(args.out)
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {len(events)} synthetic snapshots to {out_path}")


if __name__ == "__main__":
    main()
