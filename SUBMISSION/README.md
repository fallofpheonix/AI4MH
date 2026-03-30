# AI4MH Submission Package

This submission pack documents the current repository state. It is aligned with the code under `backend/`, `frontend/`, and `scripts/`.

## Package Contents

```text
SUBMISSION/
  README.md
  INSTALLATION.md
  TESTING.md
  VERIFICATION.md
  DEPLOYMENT.md
  docs/
    API_REFERENCE.md
    FEATURES.md
    GOVERNANCE.md
```

## System Summary

- Backend: FastAPI application with a versioned API under `/api/v1`
- Persistence: SQLite-backed `Store` implementation with in-memory test store
- Domain types: Pydantic models under `backend/app/schemas`
- Business logic: `backend/app/services`
- Frontend: React/Vite dashboard with modular `pages`, `hooks`, `services`, and `components`

## Current Project Shape

```text
backend/
  app/
    api/        dependencies, router, v1 routes
    core/       config, container, store factory
    crud/       persistence interfaces and implementations
    schemas/    Pydantic models
    services/   ingestion, enrichment, scoring, alerts, pipeline
    utils/      shared helpers
  tests/
frontend/
  src/
    components/
    hooks/
    pages/
    services/
    styles/
    utils/
scripts/
  full_health_check.sh
```

## Evaluator Quick Path

1. Follow [INSTALLATION.md](/Users/fallofpheonix/Project/Human AI/done/AI4MH/SUBMISSION/INSTALLATION.md).
2. Run backend tests:
   ```bash
   cd backend
   ./.venv312/bin/python -m pytest
   ```
3. Run the full-stack health check:
   ```bash
   bash scripts/full_health_check.sh
   ```
4. Open the dashboard at `http://127.0.0.1:5173`.

## API Surface

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

Endpoints:

- `POST /ingest?n=30`
- `GET /posts?limit=60`
- `GET /scores`
- `GET /alerts`
- `POST /alerts/{alert_id}/ack`
- `POST /alerts/{alert_id}/dismiss`
- `POST /alerts/{alert_id}/resolve`
- `GET /logs?limit=100`
- `GET /bias`

## Validation Targets

- Backend tests: `backend/tests/test_api.py`, `backend/tests/test_scoring.py`
- Frontend production build: `npm run build`
- End-to-end smoke check: `scripts/full_health_check.sh`

## Scope Notes

- Data is synthetic; no live social platform integration is present.
- No authentication or role system is implemented.
- Alert lifecycle actions exist through the API, not the dashboard UI.
- Deployment assets such as Dockerfiles are not included in this repository.
