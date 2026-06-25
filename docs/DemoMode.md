# Demo Mode

Demo mode lets you run and evaluate the **entire** toolkit with **no camera** and
**no real footage** — only synthetic, anonymous data.

## Enable / disable

Controlled by `ENABLE_DEMO_MODE` (default `true`).

```bash
ENABLE_DEMO_MODE=true uvicorn app.main:app --app-dir backend
```

## What it does

On startup the backend:

1. Seeds a demo camera and a generic restaurant floor plan.
2. Builds an `AnalyticsEngine` driven by a `SyntheticDetector`.
3. Starts a loop that ticks every `LIVE_UPDATE_INTERVAL_SECONDS`, broadcasting
   aggregate snapshots over `/ws/analytics` and periodically persisting
   aggregate rows + evaluating alerts.

## The synthetic detector

`SyntheticDetector` simulates anonymous "agents" that arrive at the entrance,
wait in the queue, sit at a table for a while, then leave. It emits the same
anonymous `Detection` boxes a real detector would — there is no imagery and
nothing personal. It is fully reproducible with a seed.

The result: occupancy rises and falls, the queue fills and clears, tables turn
over, the heatmap warms up, and alerts trigger — exactly what you'd see with a
real feed, minus the privacy risk.

## Generate a static timeline

```bash
python demo/synthetic/generate_synthetic_flow.py --frames 120 \
  --out demo/synthetic/sample_events.json
```

This writes an aggregate, anonymous event timeline you can inspect or replay.

## Moving to a real camera (v0.2+)

Set `ENABLE_DEMO_MODE=false` and provide a `CAMERA_SOURCE`. Real ingestion is on
the [roadmap](../ROADMAP.md); the detector interface and analytics already work
against any `Detector` implementation, so the upgrade is additive.

## Tuning the demo

`SyntheticDetector` accepts `seed`, `step_seconds`, `base_arrival_rate`, and
`max_agents`. Raise `base_arrival_rate` for a busier venue (e.g. fast food).
