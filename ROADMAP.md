# Roadmap

This roadmap is intentionally honest and incremental. Restaurant Vision
Analytics is an **early open-source toolkit**, not a finished product. Every
phase preserves the privacy-first guarantees — features that would require
identifying people are explicitly out of scope, forever.

## v0.1 — Foundation (current)

- [x] Demo mode (synthetic, anonymous customer flow — no camera needed)
- [x] Zone engine (polygons, point-in-zone, seven zone types)
- [x] Occupancy analytics (per-zone, total, peak, average)
- [x] Queue pressure analytics + alerts
- [x] Table usage (occupied/free, dwell, turnover, idle detection)
- [x] Anonymous crowd-density heatmap
- [x] Ephemeral centroid tracker (TTL, no re-identification)
- [x] FastAPI backend + WebSocket live feed
- [x] React + TypeScript dashboard (dark operations UI)
- [x] Privacy & ethics documentation
- [x] Test suite + CI
- [x] Docker Compose one-command setup

## v0.2 — Real cameras

- [ ] RTSP / device / file camera ingestion
- [ ] Improved detector adapters (documented, weights not bundled)
- [ ] Visual drag-and-drop **zone editor** in the dashboard
- [ ] Alert-rule configuration UI
- [ ] PostgreSQL support hardening
- [ ] CSV export of aggregate metrics

## v0.3 — Scale & operations

- [ ] Multi-camera support
- [ ] Historical reports (aggregate trends over time)
- [ ] Role-based access control (RBAC)
- [ ] Edge deployment guide
- [ ] More configurable retention policies

## v1.0 — Stable

- [ ] Stable, versioned public API
- [ ] Plugin detector interface (clean extension points)
- [ ] Production deployment guide (TLS, auth, scaling)
- [ ] Full privacy review checklist & audit notes
- [ ] More end-to-end examples

## Permanently out of scope

- Facial recognition / biometric identification
- Demographic, age, gender, ethnicity, or emotion inference
- Persistent per-customer tracking or re-identification
- Employee surveillance / per-person performance policing
- Audio recording

Have an idea that fits the privacy-first scope? Open a **Feature request** — see
[CONTRIBUTING.md](CONTRIBUTING.md).
