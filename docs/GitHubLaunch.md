# GitHub Launch Guide

This guide collects the repository metadata, first-release notes, starter issue
ideas, and launch-post drafts for publishing `restaurant-vision-analytics`
responsibly.

Canonical repository:
`https://github.com/huseyintkoksal/restaurant-vision-analytics`

## Repository metadata

### Description

Privacy-first computer vision toolkit for restaurant occupancy, queue
monitoring, table usage and customer flow analytics.

### Website field suggestion

Leave the Website field blank until there is a real hosted demo, project page,
or demo video. Do not point it at a temporary URL.

### Topics

- computer-vision
- privacy-first
- restaurant-analytics
- occupancy
- queue-monitoring
- heatmap
- fastapi
- react
- opencv
- self-hosted
- operations-analytics

### About section text

Privacy-first computer vision toolkit for restaurant occupancy, queue
monitoring, table usage and customer flow analytics. Runs locally, includes a
synthetic demo, and does not perform facial recognition, biometric
identification, demographic inference, emotion detection, audio recording, or
persistent customer tracking.

### Recommended repository settings

- Enable Issues.
- Enable private vulnerability reporting.
- Add the topics listed above.
- Add branch protection after the first successful GitHub Actions run.
- Keep Discussions optional until there is enough community traffic to support
  it.

## First release

### Release title

`v0.1.1 - Public release readiness`

### Release notes

```md
Restaurant Vision Analytics v0.1.1 prepares the project for a public
open-source launch.

Highlights
- Anonymous occupancy, queue pressure, table usage, and heatmap analytics
- FastAPI backend with REST endpoints and a WebSocket live feed
- React + TypeScript dashboard
- Synthetic demo mode, so the stack runs without a camera
- Privacy-first documentation, audit script, and regression tests
- Docker Compose, GitHub Actions workflows, screenshots, and a demo GIF

Privacy posture
This project does not perform facial recognition, biometric identification,
demographic inference, emotion detection, audio recording, or persistent
customer tracking. Raw frame storage is off by default.

Known limitations
- Demo mode uses synthetic data.
- Real camera/video input is experimental in v0.1.
- Accuracy depends on camera angle, lighting, occlusion, detector quality, and
  zone setup.
- This is not a legal compliance product or legal advice.
```

### Installation snippet

```bash
git clone https://github.com/huseyintkoksal/restaurant-vision-analytics.git
cd restaurant-vision-analytics
docker compose up --build
```

Manual local setup:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --app-dir backend

cd frontend
npm install
npm run dev
```

### Known limitations

- Demo mode uses synthetic data.
- RTSP and video-file sources are experimental.
- The toolkit is intended for operational estimates, not legal compliance.
- Real deployments require local privacy and legal review.
- No detector weights are bundled.

### Privacy note

This repository is designed around aggregate operational analytics. It does not
ship endpoints, database tables, or UI flows for facial recognition, biometric
identification, demographic inference, emotion detection, audio recording,
persistent customer tracking, customer profiles, or employee scoring.

## Good first issues

1. Improve Docker docs for Windows users
2. Add frontend unit tests with Vitest
3. Improve zone editor UX prototype
4. Add more synthetic demo scenarios
5. Expand troubleshooting docs

## Help wanted issues

1. Harden RTSP/video source handling
2. Add PostgreSQL deployment example
3. Add CSV export for analytics summaries
4. Add edge deployment guide
5. Add optional detector adapter documentation

## Launch posts

### Show HN

Title:

```text
Show HN: Restaurant Vision Analytics - privacy-first restaurant operations analytics
```

Post:

```text
I built Restaurant Vision Analytics, an open-source toolkit for anonymous
restaurant operations analytics: occupancy, queue pressure, table usage, and
coarse heatmaps.

The main design constraint is privacy. It does not perform facial recognition,
biometric identification, demographic inference, emotion detection, audio
recording, or persistent customer tracking. The demo runs with synthetic data,
so you can try the dashboard without a camera.

It is an early v0.1 toolkit, not a production compliance product. Feedback on
the API, privacy boundary, and analytics model would be useful.

https://github.com/huseyintkoksal/restaurant-vision-analytics
```

### Reddit r/selfhosted

```text
I am publishing an MIT-licensed, self-hosted toolkit for restaurant occupancy,
queue pressure, table usage, and customer-flow analytics.

It runs locally with FastAPI, SQLite, and a React dashboard. Demo mode uses
synthetic data, so no camera is required for first run. The project explicitly
avoids facial recognition, biometrics, demographic/emotion inference, audio
recording, and persistent customer tracking.

I would appreciate feedback from people who care about local-first operations
software and privacy-first design.

https://github.com/huseyintkoksal/restaurant-vision-analytics
```

### Reddit r/computervision

```text
I am looking for design feedback on Restaurant Vision Analytics, a privacy-first
computer vision toolkit for aggregate restaurant operations metrics.

The stack includes a detector interface, synthetic demo detector, zone polygons,
ephemeral centroid tracking, occupancy, queue pressure, table usage, and a
coarse heatmap. The analytics boundary is intentionally aggregate only: no face
recognition, biometrics, demographic/emotion inference, re-identification, or
persistent customer tracking.

Real RTSP/video input is experimental; demo mode runs without camera hardware.

https://github.com/huseyintkoksal/restaurant-vision-analytics
```

### X/Twitter short post

```text
Open-sourced Restaurant Vision Analytics: a privacy-first toolkit for restaurant
occupancy, queue monitoring, table usage, and heatmaps.

Synthetic demo, FastAPI backend, React dashboard, no facial recognition or
identity tracking.

https://github.com/huseyintkoksal/restaurant-vision-analytics
```

### LinkedIn post

```text
I am publishing Restaurant Vision Analytics, an open-source toolkit for
privacy-first restaurant operations analytics.

It focuses on aggregate signals: occupancy, queue pressure, table usage, and
coarse customer-flow heatmaps. It includes a FastAPI backend, React dashboard,
WebSocket live updates, Docker Compose, and a synthetic demo mode.

The important boundary: it does not perform facial recognition, biometric
identification, demographic inference, emotion detection, audio recording, or
persistent customer tracking. Raw frame storage is off by default.

This is an early toolkit, not a legal compliance product, and real deployments
still require local privacy review. Feedback and contributions are welcome.

https://github.com/huseyintkoksal/restaurant-vision-analytics
```

## Responsible launch rules

- No bought stars.
- No bots.
- No star exchanges.
- No engagement spam.
- No misleading claims.
- No surveillance marketing.
- Follow each community's self-promotion rules.
- Answer questions transparently and fix documentation mistakes quickly.
