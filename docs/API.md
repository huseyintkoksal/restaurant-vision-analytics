# API Reference

Every endpoint returns aggregate, anonymous operational data. There are no
endpoints for faces, identities, demographics, emotions, audio, customer
profiles, employee scoring, or per-person history.

## Base URL

Local development:

```text
http://localhost:8000
```

Interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication note

v0.1 is a local/demo toolkit and does not include built-in authentication. For
any shared or production-like deployment, put the API and dashboard behind a
reverse proxy, VPN, SSO gateway, or equivalent access-control layer. Do not
expose an unauthenticated instance to the public internet.

## Health endpoint

### `GET /health`

Returns liveness, version, demo mode, and the privacy posture.

```json
{
  "status": "ok",
  "version": "0.1.1",
  "app_env": "development",
  "demo_mode": true,
  "time": "2026-01-01T12:00:00Z",
  "privacy": {
    "facial_recognition": false,
    "biometric_identification": false,
    "demographic_inference": false,
    "emotion_detection": false,
    "audio_recording": false,
    "persistent_customer_tracking": false,
    "raw_frame_storage": false
  },
  "privacy_statement": "This project does not perform facial recognition, biometric identification, demographic inference, emotion detection, audio recording, or persistent customer tracking."
}
```

## Cameras endpoints

### `GET /api/cameras`

Lists configured camera records. Camera records describe where analytics run.
They do not store credentials or captured imagery.

```json
[
  {
    "id": "demo-camera-1",
    "name": "Demo Camera",
    "location": "Front of house",
    "status": "online",
    "source_type": "demo",
    "created_at": "2026-01-01T12:00:00Z",
    "last_seen": null
  }
]
```

### `POST /api/cameras`

Creates a camera configuration. Credentials are intentionally not accepted.

```json
{
  "name": "Front of House",
  "location": "Main floor",
  "status": "unknown",
  "source_type": "demo"
}
```

Response: `201 Created` with the created camera record.

### `GET /api/cameras/{camera_id}`

Returns one camera record or `404` if it does not exist.

## Zones endpoints

### `GET /api/zones`

Lists configured zones. Optional query parameter: `camera_id`.

```json
[
  {
    "id": "queue-1",
    "name": "Order Queue",
    "type": "queue",
    "camera_id": "demo-camera-1",
    "capacity": 6,
    "polygon": [[0.18, 0.5], [0.42, 0.5], [0.42, 0.74], [0.18, 0.74]],
    "attributes": {}
  }
]
```

### `POST /api/zones`

Creates a named polygon zone.

```json
{
  "name": "Order Queue",
  "type": "queue",
  "camera_id": "demo-camera-1",
  "capacity": 6,
  "polygon": [[0.18, 0.5], [0.42, 0.5], [0.42, 0.74], [0.18, 0.74]],
  "attributes": {}
}
```

Current zone types are `entrance`, `dining_area`, `table`, `queue`, `cashier`,
`kitchen_pass`, and `pickup_area`.

## Analytics endpoints

### `GET /api/analytics/live`

Returns the latest live aggregate snapshot.

### `GET /api/analytics/summary`

Returns session-level aggregate metrics: estimated visitors, peak/average
occupancy, peak hour, table summary, and privacy flags.

### `GET /api/analytics/heatmap`

Returns a coarse anonymous density grid.

### `GET /api/analytics/tables`

Returns per-table occupied/free state and aggregate table summary.

### `GET /api/analytics/queue`

Returns current queue count, pressure score, status, and estimated wait
pressure.

### `GET /api/analytics/history`

Returns recent occupancy/queue time series for charts.

```json
{
  "series": [
    {
      "timestamp": "2026-01-01T12:00:00Z",
      "total": 18,
      "queue_count": 5,
      "queue_pressure": 0.833
    }
  ]
}
```

## Alerts endpoints

### `GET /api/alerts`

Lists recent operational alerts.

Query parameters:

- `limit`: integer from `1` to `500`, default `50`
- `unresolved_only`: boolean, default `false`

```json
[
  {
    "id": 12,
    "type": "queue_too_long",
    "severity": "warning",
    "message": "Queue pressure high (85%).",
    "camera_id": "demo-camera-1",
    "zone_id": "queue-1",
    "value": 0.85,
    "created_at": "2026-01-01T12:00:00Z",
    "resolved": false
  }
]
```

## Privacy endpoint

### `GET /api/privacy`

Returns machine-readable privacy guarantees used by the dashboard.

## WebSocket endpoint

### `WS /ws/analytics`

Streams aggregate live analytics snapshots. The server sends the current
snapshot immediately after connection and then sends periodic updates on the
configured live-update interval. The feed is read-only.

## Error response format

FastAPI returns standard JSON error payloads.

```json
{
  "detail": "Camera not found"
}
```

Validation errors use the FastAPI/Pydantic `detail` array format.

Common status codes:

- `404`: resource not found
- `422`: malformed request body or query parameter
- `500`: unexpected server error

## Live analytics response example

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "camera_id": "demo-camera-1",
  "occupancy": {
    "total": 18,
    "by_zone": {
      "entrance-1": 1,
      "queue-1": 5,
      "cashier-1": 1,
      "dining-1": 11,
      "table-1": 2
    },
    "by_type": {
      "entrance": 1,
      "queue": 5,
      "cashier": 1,
      "dining_area": 11,
      "table": 2
    }
  },
  "queue": {
    "count": 5,
    "pressure_score": 0.833,
    "status": "congested",
    "estimated_wait_pressure": "very_high"
  },
  "tables": [
    {
      "zone_id": "table-1",
      "name": "Table 1",
      "occupied": true,
      "duration_seconds": 1320,
      "turnover_count": 3,
      "idle": false
    }
  ],
  "active_tracks": 18,
  "privacy": {
    "identity_tracking": false,
    "biometrics": false,
    "raw_frame_storage": false
  }
}
```

## Queue response example

`GET /api/analytics/queue`

```json
{
  "count": 5,
  "pressure_score": 0.833,
  "status": "congested",
  "estimated_wait_pressure": "very_high"
}
```

`status` is one of `clear`, `moderate`, `busy`, or `congested`.
`estimated_wait_pressure` is one of `low`, `medium`, `high`, or `very_high`.

## Table response example

`GET /api/analytics/tables`

```json
{
  "tables": [
    {
      "zone_id": "table-1",
      "name": "Table 1",
      "occupied": true,
      "duration_seconds": 1320,
      "turnover_count": 3,
      "idle": false
    }
  ],
  "summary": {
    "tables": 6,
    "occupied": 4,
    "free": 2,
    "occupancy_rate": 0.667,
    "total_turnovers": 11,
    "avg_occupied_duration_seconds": 840
  }
}
```

## Heatmap response example

`GET /api/analytics/heatmap`

```json
{
  "rows": 12,
  "cols": 16,
  "max": 4.3812,
  "cells": [
    [0.0, 0.12, 0.44],
    [0.08, 0.91, 0.33]
  ]
}
```

`cells` is a normalized density grid in `[0, 1]`. It represents where crowds
form, never who was there.

## Privacy response example

`GET /api/privacy`

```json
{
  "facial_recognition": false,
  "biometric_identification": false,
  "demographic_inference": false,
  "emotion_detection": false,
  "audio_recording": false,
  "persistent_customer_tracking": false,
  "raw_frame_storage": false,
  "identity_persistence": false,
  "ephemeral_tracking": true,
  "local_first": true,
  "data_retention_days": 7,
  "statement": "This project does not perform facial recognition, biometric identification, demographic inference, emotion detection, audio recording, or persistent customer tracking."
}
```

## Demo mode notes

- `ENABLE_DEMO_MODE=true` by default.
- Demo mode uses synthetic, anonymous customer-flow data.
- No camera is required for first run, screenshots, GIFs, tests, or CI.
- Tune demo intensity with `DEMO_ARRIVAL_RATE`.
- Tune live update cadence with `LIVE_UPDATE_INTERVAL_SECONDS`.
- Use `DEMO_SEED` for reproducible demo runs.

## Privacy guarantees

- No facial recognition.
- No biometric identification.
- No demographic inference.
- No emotion detection.
- No audio recording.
- No persistent customer tracking.
- No customer profile database.
- No employee scoring.
- Raw frame storage is off by default.
- Analytics outputs are aggregate operational metrics.

## Limitations

- This is an early v0.1 toolkit.
- Demo mode uses synthetic data.
- Real RTSP/video-file input is experimental.
- Accuracy depends on camera angle, lighting, occlusion, detector quality, and
  zone setup.
- Built-in authentication is not included in v0.1.
- This is not a legal compliance product and not legal advice.
- Real deployments require local legal and privacy review.
