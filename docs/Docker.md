# Docker

The fastest way to see the whole stack running.

## One command

```bash
docker compose up --build
```

- Backend → http://localhost:8000 (FastAPI, demo data, WebSocket)
- Frontend → http://localhost:5173 (dashboard)
- SQLite persists in the named volume `rva-data` (mounted at `/data`)

Stop and remove:

```bash
docker compose down
# add -v to also remove the data volume:
docker compose down -v
```

## What the Compose file does

- **backend** builds from `backend/Dockerfile` (Python 3.11 slim), runs as a
  non-root user, exposes `:8000`, and stores its SQLite DB in `/data`. Privacy
  env defaults are set explicitly (`ENABLE_RAW_FRAME_STORAGE=false`,
  `DATA_RETENTION_DAYS=7`).
- **frontend** builds from `frontend/Dockerfile` (Node 20 alpine) and serves the
  Vite dev server on `:5173`, pointed at the backend via `VITE_API_BASE_URL`.

## Validate the configuration

```bash
docker compose config        # render & validate the merged config
docker compose build         # build images without starting
```

## Customizing

Override environment in `docker-compose.yml` or with an `.env` file. For
example, to change the retention window:

```yaml
services:
  backend:
    environment:
      DATA_RETENTION_DAYS: "14"
```

## Notes

- The bundled images are tuned for **demo/development**. For production, front
  the services with TLS and authentication and consider a static build of the
  frontend served by a CDN or nginx.
- No raw frames are written inside the container; only aggregate metrics land in
  the `rva-data` volume.
