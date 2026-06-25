# Getting Started

This guide takes you from a fresh clone to a live dashboard fed by synthetic,
anonymous data — no camera required.

## Requirements

- **Python** 3.11 or newer
- **Node.js** 18 or newer (20+ recommended)
- **Git**
- (Optional) **Docker** + Docker Compose for the one-command path

## 1. Clone

```bash
git clone https://github.com/huseyintkoksal/restaurant-vision-analytics.git
cd restaurant-vision-analytics
cp .env.example .env   # safe defaults: demo mode on, raw frames off
```

## 2. Backend setup

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -e ".[dev]"
uvicorn app.main:app --reload --app-dir backend
```

The API is now on **http://localhost:8000**. Visit:

- http://localhost:8000/health — liveness + privacy posture
- http://localhost:8000/docs — interactive OpenAPI docs

## 3. Frontend setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The dashboard connects to the backend over REST
and a WebSocket and starts updating immediately.

## 4. Docker setup (alternative)

```bash
docker compose up --build
# backend  -> http://localhost:8000
# frontend -> http://localhost:5173
```

See [Docker.md](Docker.md) for details.

## 5. Demo mode

Demo mode is **on by default** (`ENABLE_DEMO_MODE=true`). A synthetic detector
simulates anonymous customer flow so every panel — occupancy, queue, tables,
heatmap, alerts — comes alive without hardware. See [DemoMode.md](DemoMode.md).

## 6. Your first analytics response

```bash
curl http://localhost:8000/api/analytics/live | jq
```

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "camera_id": "demo-camera-1",
  "occupancy": { "total": 18, "by_zone": { "entrance": 2, "queue": 5, "dining_area": 11 } },
  "queue": { "count": 5, "pressure_score": 0.72, "status": "busy" },
  "tables": [{ "zone_id": "table-1", "occupied": true, "duration_seconds": 1320 }],
  "privacy": { "identity_tracking": false, "biometrics": false, "raw_frame_storage": false }
}
```

## 7. Run the tests

```bash
pytest
```

## Troubleshooting

If something doesn't line up, see [Troubleshooting.md](Troubleshooting.md).
