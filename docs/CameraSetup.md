# Camera Setup

> **v0.1 ships demo mode only.** Real camera ingestion (RTSP/device/file) is on
> the [roadmap](../ROADMAP.md) for v0.2. This page documents the model and how to
> prepare, so the upgrade is smooth.

## Configuration vs. credentials

A camera **record** in this system is configuration only — a name, a location, a
status, and a source type. **Credentials are never stored in the database.**
When real ingestion lands, connection secrets (e.g. an RTSP password) must come
from environment variables or a secrets manager and are read at runtime.

```bash
# Example (kept out of git, provided at runtime):
export CAMERA_SOURCE="rtsp://CAMERA_HOST:554/stream"
```

## Creating a camera record

```bash
curl -X POST http://localhost:8000/api/cameras \
  -H "Content-Type: application/json" \
  -d '{"name":"Front of House","location":"Main floor","source_type":"demo"}'
```

`source_type` is one of `demo | rtsp | file | device`. No password field exists
on this endpoint.

## Placement guidance (for good *anonymous* analytics)

- Mount **high and angled down** so people separate well in the frame; this
  improves anonymous counting and zone assignment.
- Frame the **operational areas** you care about (entrance, queue, tables).
- Favor wide coverage of *spaces* over tight shots of *faces* — the pipeline
  needs floor positions, not portraits.
- Ensure even lighting to stabilize detection.

## Signage

Where a camera operates, post a clear, visible notice. See
[KVKK_GDPR_Checklist.md](KVKK_GDPR_Checklist.md) and
[EthicsAndResponsibleUse.md](EthicsAndResponsibleUse.md).

## What the camera is **not** used for

No facial recognition, no biometric capture, no recording of individuals, no
demographic or emotion inference. The camera supplies frames; the pipeline emits
only anonymous counts. Raw frames are not stored by default.
