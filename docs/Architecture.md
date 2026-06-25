# Architecture

## Monorepo structure

```
restaurant-vision-analytics/
├── backend/      FastAPI app, vision pipeline, analytics engine, tests
├── frontend/     React + TypeScript + Vite dashboard
├── demo/         Synthetic generator + example floor plans
├── docs/         You are here
└── examples/     Ready-to-run scenarios
```

## Backend architecture

Layered, with a strict privacy boundary between detection and analytics:

```
            ┌─────────────────────────────────────────────┐
 Frame ───▶ │ Detector (Mock/Synthetic | OpenCV | adapter) │  ── anonymous boxes
            └─────────────────────────────────────────────┘
                              │  Detection(bbox, confidence, "person")
                              ▼
            ┌─────────────────────────────────────────────┐
            │ AnalyticsEngine                              │
            │  • CentroidTracker (ephemeral ids, TTL)      │
            │  • Occupancy / Queue / TableUsage / Heatmap  │
            └─────────────────────────────────────────────┘
                              │  aggregate snapshot (numbers only)
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         WebSocket      REST API      SQLite/Postgres
         (live feed)   (/api/...)    (aggregate rows)
```

Key modules:

- `app/vision/detector_base.py` — the `Detector` interface and the anonymous
  `Detection` value object.
- `app/vision/analytics_engine.py` — orchestrates detection + analytics into
  aggregate snapshots.
- `app/services/analytics_service.py` — owns the engine, the demo loop, and the
  realtime fan-out.
- `app/api/*` — thin FastAPI routers.
- `app/models/*` — SQLModel tables (cameras, zones, snapshots, alerts) — no
  person/identity tables exist.

## Frontend architecture

- **React + TypeScript + Vite**, styled with **Tailwind CSS**.
- `src/api/client.ts` — typed REST client.
- `src/api/websocket.ts` — auto-reconnecting live feed.
- `src/components/*` — presentational panels (metrics, charts, table map,
  heatmap, alerts).
- `src/pages/*` — Dashboard, Cameras, Zones, Privacy, Settings.

State is intentionally simple: the live WebSocket drives fast-moving panels;
short polls refresh slower aggregates (summary, history, alerts).

## Vision pipeline

1. A `Detector` returns anonymous `Detection` boxes for a frame.
2. Foot points (bottom-center of each box) are computed for floor position.
3. The `CentroidTracker` associates points across frames with **ephemeral** ids
   to estimate flow. No re-identification, no persistence.
4. Analytics modules turn points + zones into aggregate metrics.

## Data flow

Detector → foot points → tracker (ephemeral) → analytics modules → aggregate
snapshot → {WebSocket, REST, database}. Only numbers cross into storage.

## Privacy boundary

The boundary sits at the `Detector` output: everything downstream sees only
anonymous geometry and counts. There is no code path from a frame to an
identity, biometric template, or demographic label. See
[PrivacyFirstDesign.md](PrivacyFirstDesign.md).

## Detector interface

```python
class Detector(ABC):
    @property
    @abstractmethod
    def info(self) -> DetectorInfo: ...

    @abstractmethod
    def detect(self, frame) -> list[Detection]: ...
```

Swap detectors without touching analytics. `SyntheticDetector` (default),
`OpenCVHOGDetector` (optional), or your own adapter (e.g. a YOLO wrapper) all
satisfy the same contract.

## Tracker lifecycle

- A new point with no nearby track → new ephemeral id.
- A matched point → the existing track is updated.
- A track with no detection for `TRACK_TTL_SECONDS` → permanently forgotten.
- A returning person → a brand-new id (no memory).

## Database design

Four tables, all configuration or aggregate:

| Table | Purpose |
| --- | --- |
| `cameras` | Camera configuration (no credentials). |
| `zones` | Named polygons (places, not people). |
| `analytics_snapshots` | Aggregate counts/pressures over time. |
| `alerts` | Operational alerts. |

## WebSocket live updates

`/ws/analytics` streams the same aggregate snapshot the demo loop produces. New
clients receive the current snapshot immediately, then updates at
`LIVE_UPDATE_INTERVAL_SECONDS`.
