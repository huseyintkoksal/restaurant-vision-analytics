# ---------------------------------------------------------------------------
# Backend image — FastAPI + Uvicorn (demo mode by default, no camera required)
# Build context is the repository root: docker build -f backend/Dockerfile .
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install runtime dependencies first for better layer caching.
COPY pyproject.toml README.md ./
COPY backend/ ./backend/

RUN python -m pip install --upgrade pip \
    && python -m pip install ".[dev]"

# Aggregated, anonymous metrics live here; raw frames are never written.
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8000

# Non-root user for safer container runtime.
RUN useradd --create-home --uid 10001 appuser && chown -R appuser /data /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "backend"]
