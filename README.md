# AI4MH

AI4MH is a full-stack demo for regional mental-health crisis signal monitoring. The system ingests synthetic discussion posts, enriches them with sentiment and keyword signals, aggregates regional scores, persists alert state in SQLite, and exposes the results through a FastAPI API and a React dashboard.

Supported local Python versions: `3.10` to `3.12`

## Scope

- Synthetic ingestion only. There are no live social-media connectors.
- Alerts are decision-support outputs, not automated intervention.
- Storage is local SQLite for demo reproducibility.

## Repository Layout

```text
backend/   FastAPI service, scoring pipeline, persistence, tests
frontend/  React/Vite dashboard
data/      Minimal runtime sample data
docs/      Architecture, API, and demo notes
scripts/   Development smoke checks
```

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Backend default address: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Frontend default address: `http://127.0.0.1:5173`

### Full Stack Smoke Check

From the repo root:

```bash
bash scripts/full_health_check.sh
```

This script can bootstrap local backend/frontend dependencies, start both services, and validate the HTTP surface.

## Common Commands

```bash
make backend-install
make frontend-install
make dev-backend
make dev-frontend
make test
make build
make smoke
```

## Docker Compose

```bash
docker compose up --build
```

This starts:

- backend on `http://localhost:8000`
- frontend on `http://localhost:80`

## API Surface

Base URL: `http://127.0.0.1:8000/api/v1`

- `POST /ingest?n=30`
- `GET /posts?limit=20`
- `GET /scores`
- `GET /alerts`
- `POST /alerts/{alert_id}/ack`
- `POST /alerts/{alert_id}/dismiss`
- `POST /alerts/{alert_id}/resolve`
- `GET /logs?limit=20`
- `GET /bias`

Detailed endpoint documentation: [docs/api.md](docs/api.md)

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Demo Notes](docs/demo.md)

## Validation

Backend tests:

```bash
make test
```

Frontend production build:

```bash
make build
```
