# ---------------------------------------------------------------------------
# Frontend image — Vite dev server for the analytics dashboard.
# Build context is the repository root: docker build -f frontend/Dockerfile .
# ---------------------------------------------------------------------------
FROM node:20-alpine

WORKDIR /app/frontend

# Install dependencies first for better layer caching.
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy the rest of the frontend source.
COPY frontend/ ./

EXPOSE 5173

# Bind to 0.0.0.0 so the dev server is reachable from the host.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
