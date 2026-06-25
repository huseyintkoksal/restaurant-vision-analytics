# Troubleshooting

## Backend won't start

- **Wrong Python version:** requires 3.11+. Check `python --version`.
- **Dependencies missing:** `pip install -e ".[dev]"` from the repo root.
- **Run from the right place:** `uvicorn app.main:app --app-dir backend` (note
  `--app-dir backend`), or `make backend`.

## `ModuleNotFoundError: app`

You're not pointing Python at the `backend/` directory. Use `--app-dir backend`,
or `pip install -e .` (which exposes the `app` package via the configured
`package-dir`).

## Dashboard shows "Backend unreachable"

- Is the backend running on `http://localhost:8000`? Open `/health`.
- **CORS:** ensure your dashboard origin is in `CORS_ORIGINS`.
- **Custom API URL:** set `VITE_API_BASE_URL` for the frontend if the backend
  isn't on `localhost:8000`.

## WebSocket keeps reconnecting

- The client auto-reconnects every 2s if the socket drops. Confirm the backend
  is up and reachable, and that any proxy in front allows WebSocket upgrades.

## No data on the dashboard

- Confirm `ENABLE_DEMO_MODE=true` (default).
- Hit `GET /api/analytics/live` directly to see if the engine is producing
  snapshots.
- Early after startup, occupancy may be 0 for a few seconds while synthetic
  agents arrive.

## Frontend build fails

- Use Node 18+ (20+ recommended): `node --version`.
- Reinstall: delete `frontend/node_modules` and run `npm install`.
- Type errors: `npm run lint` (runs `tsc --noEmit`) to see details.

## Tests fail to find the database

- Tests configure their own temporary SQLite database in
  `backend/tests/conftest.py`. If you overrode `DATABASE_URL` in your shell,
  unset it before running `pytest`.

## OpenCV import errors

- OpenCV is an **optional** extra. Install it only if you use
  `OpenCVHOGDetector`: `pip install ".[opencv]"`. The default demo path does not
  need it.

## Docker issues

- `docker compose config` to validate the file.
- Port conflicts on 8000/5173: stop the conflicting process or remap ports in
  `docker-compose.yml`.

Still stuck? Open an issue with your OS, Python/Node versions, and the full error
output. See [CONTRIBUTING.md](../CONTRIBUTING.md).
