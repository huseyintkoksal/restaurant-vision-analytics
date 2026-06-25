# Deployment

This is an **early open-source toolkit**, not a turnkey production product. The
guidance below helps you run it safely on your own infrastructure. Prefer
**local-first** deployments.

## Topologies

### Single-node (recommended for most venues)
Backend + frontend + SQLite on one on-prem machine. No customer data leaves the
premises. Use Docker Compose ([Docker.md](Docker.md)) or run each service
directly.

### Backend + Postgres
For multiple cameras/venues or longer aggregate history, point
`DATABASE_URL` at PostgreSQL:

```bash
pip install ".[postgres]"
export DATABASE_URL="postgresql+psycopg://user:pass@db-host:5432/rva"
```

## Configuration

All configuration is environment-driven (see [`.env.example`](../.env.example)):

| Variable | Default | Notes |
| --- | --- | --- |
| `APP_ENV` | `development` | `production` in prod. |
| `DATABASE_URL` | local SQLite | Postgres optional. |
| `ENABLE_DEMO_MODE` | `true` | Turn **off** for real ingestion (v0.2+). |
| `ENABLE_RAW_FRAME_STORAGE` | `false` | Keep off unless audited. |
| `DATA_RETENTION_DAYS` | `7` | Aggregate retention window. |
| `CORS_ORIGINS` | localhost | Set to your dashboard origin. |

## Production hardening

- Run the backend behind a reverse proxy (TLS termination, timeouts).
- Restrict `CORS_ORIGINS` to your dashboard's real origin.
- Put the dashboard and API behind authentication (role-based access is on the
  roadmap; until then, restrict network access).
- Provide camera/DB secrets via environment variables or a secrets manager —
  never commit them.
- Keep `ENABLE_RAW_FRAME_STORAGE=false`.
- Set a retention window appropriate to your policy and local law.

## Process model

The backend runs the analytics/demo loop as an asyncio task inside the FastAPI
app. For a single-camera demo this is sufficient. Multi-camera orchestration and
edge deployment guides are planned (see [ROADMAP.md](../ROADMAP.md)).

## Health checks

Point your orchestrator at `GET /health` (the bundled Docker image already
includes a healthcheck).

## Backups

Back up the SQLite file (or your Postgres database). It contains only aggregate,
anonymous metrics and configuration — no personal data.
