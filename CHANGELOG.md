# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Upcoming changes will be listed here (see [ROADMAP.md](ROADMAP.md)).

## [0.1.1] - 2026-06-26

Public release readiness polish.

### Added

- Public launch guide with repository metadata, issue ideas, release notes, and
  responsible launch-post drafts.
- Detailed v0.2 plan and demo recording guide.
- Release verification and privacy audit tooling for launch checks.
- Curated demo screenshots, dashboard GIF, and architecture/privacy diagrams.

### Changed

- Updated repository links to the canonical
  `huseyintkoksal/restaurant-vision-analytics` owner.
- Completed API documentation with endpoint-specific examples and privacy
  limitations.
- Marked RTSP/video-file frame sources as experimental and optional for v0.1.

## [0.1.0] - 2026-06-25

Initial open-source release scaffold.

### Added

- **Privacy-first vision pipeline**: pluggable `Detector` interface, anonymous
  `Detection` value object, ephemeral centroid tracker (TTL, no
  re-identification), and zone engine (point-in-polygon, seven zone types).
- **Analytics**: occupancy (per-zone, total, peak, average), queue pressure with
  status bands, table usage (occupied/free, dwell, turnover, idle detection),
  and an anonymous crowd-density heatmap.
- **Demo mode**: a `SyntheticDetector` that simulates anonymous customer flow so
  the entire stack runs with no camera and no real footage.
- **Backend**: FastAPI app with health, cameras, zones, analytics, alerts
  endpoints, a `/ws/analytics` WebSocket live feed, SQLModel models (SQLite
  default, Postgres optional), retention service, and edge-triggered alerts.
- **Frontend**: React + TypeScript + Vite + Tailwind dashboard with live
  occupancy, queue pressure, table map, heatmap, alerts, camera health, and a
  privacy badge; Cameras, Zones, Privacy, and Settings pages.
- **Privacy controls**: raw-frame storage off by default, configurable
  retention, debug-frame anonymizer (blur/mask), and privacy guarantees surfaced
  via `/health` and `/api/privacy`.
- **Docs**: getting started, architecture, privacy-first design, ethics,
  camera/zone setup, analytics model, API reference, deployment, Docker, data
  retention, KVKK/GDPR checklist, demo mode, troubleshooting, and a star-ready
  checklist.
- **Tooling**: pytest suite (incl. privacy regression tests), ruff config,
  Docker Compose, Makefile, GitHub Actions (backend, frontend, docker), issue/PR
  templates, and example floor plans.

[Unreleased]: https://github.com/huseyintkoksal/restaurant-vision-analytics/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/huseyintkoksal/restaurant-vision-analytics/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/huseyintkoksal/restaurant-vision-analytics/releases/tag/v0.1.0
