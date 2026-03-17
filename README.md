# AI4MH

AI4MH is a small crisis-monitoring demo: it generates synthetic posts, enriches them with sentiment and keyword signals, scores regions, and exposes the results through a FastAPI backend and a React dashboard.

## What it does

- ingests synthetic mental-health discussion posts
- scores regions using sentiment, volume, clustering, and trend signals
- creates review alerts when signal strength crosses a threshold
- keeps a simple audit trail for ingest and alert transitions

## Project shape

```text
backend/
  app/
    api/       HTTP routes and request wiring
    config/    runtime settings
    core/      domain models and storage contracts
    services/  ingestion, enrichment, scoring, alert workflows
    utils/     small shared helpers
  tests/       critical-path tests
frontend/
  src/         dashboard UI
```

## Run locally

```bash
cd backend
python3 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

In another shell:

```bash
cd frontend
npm install
npm run dev
```

Backend runs on `http://localhost:8000` and the dashboard runs on `http://localhost:5173`.

## Tests

```bash
cd backend
source .venv312/bin/activate
pytest
```

## A few decisions

- The backend keeps a thin API layer and pushes behavior into services.
- SQLite is enough here; the store contract is deliberately small so it can be swapped later.
- The scoring model is intentionally simple and explainable. It is not trying to be statistically clever.
