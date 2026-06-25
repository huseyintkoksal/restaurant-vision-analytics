# v0.2 Plan

This is a scoped, privacy-first plan for the next milestone. Every item keeps
analytics aggregate and anonymous. No item adds facial recognition, biometric
identification, demographic inference, emotion detection, re-identification, or
persistent customer tracking.

## 1. RTSP/video file input hardening

**Purpose:** Make the experimental real-input path reliable enough for early
field testing.

**Scope:** Add reconnect/backoff behavior, read timeouts, frame-drop handling,
FPS throttling, and clear operator errors.

**Files likely affected:** `backend/app/vision/sources/*`,
`backend/app/services/analytics_service.py`, `backend/app/config.py`,
`docs/CameraSetup.md`, `docs/Troubleshooting.md`.

**Acceptance criteria:** A dropped RTSP stream retries without crashing the app;
missing OpenCV produces a clear error; unreachable sources do not leak
credential-bearing URLs; tests cover graceful failure paths.

**Privacy boundary:** Camera credentials come from environment variables or a
secret manager only. Raw frame storage remains off by default.

**Risks:** OpenCV behavior differs across Windows, Linux, GPU images, and
container environments.

## 2. Detector plugin adapter

**Purpose:** Let users integrate their own detector without changing core
analytics code or bundling model weights.

**Scope:** Add a detector registry, configuration selection, adapter
documentation, and one minimal example adapter.

**Files likely affected:** `backend/app/vision/detector_base.py`,
`backend/app/vision/opencv_hog_detector.py`, `backend/app/config.py`,
`docs/Architecture.md`, `docs/CameraSetup.md`, `LICENSES.md`.

**Acceptance criteria:** A detector can be selected by configuration; adapters
return anonymous boxes only; optional weights are user-supplied and ignored by
git; tests cover registry selection.

**Privacy boundary:** Detector adapters may emit anonymous bounding boxes and
confidence values only. They must not emit identities, faces, demographics,
emotions, or biometric features.

**Risks:** Third-party model licensing, model size, dependency conflicts, and
users accidentally choosing invasive detectors.

## 3. Zone editor UI

**Purpose:** Make zone setup possible from the dashboard instead of hand-editing
JSON or using curl.

**Scope:** Add a visual polygon editor, vertex drag handles, create/delete
flows, validation, and save/load through the existing zones API.

**Files likely affected:** `frontend/src/pages/Zones.tsx`,
`frontend/src/api/client.ts`, `frontend/src/types/analytics.ts`,
`frontend/src/components/*`, `backend/app/api/zones.py`.

**Acceptance criteria:** A user can create, edit, and save queue/table/dining
zones; coordinates stay normalized; invalid polygons are rejected with helpful
UI feedback.

**Privacy boundary:** Zones describe places only. The editor must not introduce
person labels, customer profiles, or identity-related fields.

**Risks:** Overlapping zones, mobile usability, coordinate transforms, and
persisting partially invalid polygons.

## 4. Alert rule editor

**Purpose:** Let operators tune queue, occupancy, and idle-table thresholds
without editing code.

**Scope:** Add alert-rule storage, CRUD endpoints, dashboard controls, and
evaluator integration.

**Files likely affected:** `backend/app/models/alert.py`,
`backend/app/services/alert_service.py`, `backend/app/api/alerts.py`,
`backend/app/database/repositories.py`, `frontend/src/pages/Settings.tsx`,
`frontend/src/components/AlertList.tsx`.

**Acceptance criteria:** A threshold changed in the UI affects future alerts;
defaults match v0.1 behavior; tests cover rule persistence and evaluator output.

**Privacy boundary:** Alerts remain about zones, queues, tables, cameras, and
aggregate conditions only.

**Risks:** Rule migration, confusing thresholds, duplicate alerts, and noisy
notifications.

## 5. PostgreSQL hardening

**Purpose:** Support longer-running deployments and multi-camera history with a
more durable database option.

**Scope:** Verify PostgreSQL connection strings, indexes, pooling, timestamps,
Docker examples, and documentation.

**Files likely affected:** `backend/app/database/*`,
`backend/app/models/*`, `docker-compose.yml`, `docs/Deployment.md`,
`docs/Docker.md`, `.github/workflows/backend.yml`.

**Acceptance criteria:** The backend test suite passes against PostgreSQL; docs
show a complete local Postgres run; indexes support common summary queries.

**Privacy boundary:** PostgreSQL stores the same aggregate/config records as
SQLite. It must not add raw frames, identities, or person-level rows.

**Risks:** SQL dialect differences, migration complexity, timezone handling, and
operator misconfiguration.

## 6. CSV export

**Purpose:** Let users analyze aggregate snapshots outside the dashboard.

**Scope:** Add an export endpoint, date filters, CSV streaming, and a dashboard
download action.

**Files likely affected:** `backend/app/api/analytics.py`,
`backend/app/database/repositories.py`,
`backend/app/models/analytics_snapshot.py`, `frontend/src/api/client.ts`,
`frontend/src/pages/Dashboard.tsx`.

**Acceptance criteria:** `GET /api/analytics/export.csv` returns aggregate-only
columns; large exports stream safely; tests prove no person-level fields exist.

**Privacy boundary:** CSV rows contain aggregate timestamps, counts, queue
metrics, table summaries, and zone IDs only.

**Risks:** Large downloads, timezone expectations, spreadsheet formatting, and
privacy regressions if nested payloads are exported without review.

## 7. Basic admin/auth mode

**Purpose:** Protect the dashboard and API for shared or remote deployments.

**Scope:** Add optional auth, admin/read-only roles, token configuration, login
UI, and deployment documentation.

**Files likely affected:** `backend/app/main.py`, `backend/app/config.py`,
`backend/app/api/*`, `frontend/src/App.tsx`, `frontend/src/api/client.ts`,
`docs/Deployment.md`, `SECURITY.md`.

**Acceptance criteria:** Auth is optional in local demo mode; when enabled,
unauthenticated requests are rejected; secrets are supplied by environment and
never committed.

**Privacy boundary:** Auth controls access only. It does not add user behavior
tracking, customer tracking, or biometric identity features.

**Risks:** Secret handling, CORS, browser storage choices, and accidentally
breaking the zero-config demo.

## 8. Frontend tests

**Purpose:** Add confidence for dashboard changes and reduce regressions.

**Scope:** Introduce Vitest, Testing Library, API-client mocks, component tests,
and a CI command.

**Files likely affected:** `frontend/package.json`, `frontend/src/**/*.test.tsx`,
`frontend/vite.config.ts`, `.github/workflows/frontend.yml`.

**Acceptance criteria:** `npm test` runs locally and in CI; dashboard cards,
privacy page, and API-client error states have starter coverage.

**Privacy boundary:** Tests should assert that privacy-off guarantees remain
visible in the UI.

**Risks:** WebSocket test flakiness and slow CI.

## 9. Better demo media

**Purpose:** Make launch visuals repeatable and easier for contributors to
refresh.

**Scope:** Add a scripted capture guide or helper, improve synthetic scenarios,
and keep GIF/screenshot sizes reasonable.

**Files likely affected:** `demo/`, `docs/RecordingDemo.md`,
`demo/synthetic/generate_synthetic_flow.py`, `README.md`.

**Acceptance criteria:** A contributor can regenerate screenshots and a short
GIF from demo mode; generated assets use synthetic data and stay within repo
size limits.

**Privacy boundary:** Demo media must never include real customers, real staff,
or real camera footage.

**Risks:** Browser automation dependencies, asset bloat, and inconsistent
rendering across machines.

## 10. Edge deployment guide

**Purpose:** Help users run the stack locally near the camera source.

**Scope:** Document mini-PC and Jetson-class deployments, resource sizing,
systemd/docker options, backups, and local network access.

**Files likely affected:** `docs/Deployment.md`, `docs/Docker.md`,
`docs/CameraSetup.md`, `docker-compose.yml`.

**Acceptance criteria:** A user can follow the guide to run backend and
dashboard on a local edge machine without cloud services.

**Privacy boundary:** The guide reinforces local-first operation and does not
recommend cloud video upload by default.

**Risks:** Hardware variance, GPU driver issues, thermal throttling, and
operator network/security configuration.
