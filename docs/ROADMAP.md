# AI4MH Roadmap

## Current State

Implemented:

- synthetic ingestion in `backend/app/services/ingestion_service.py`
- VADER enrichment and crisis keyword matching
- region scoring with sentiment, volume, geo-cluster, and trend components
- confidence calculation and escalation gating
- alert lifecycle management with append-only log events
- versioned API routes under `backend/app/api/v1`
- persistence behind `backend/app/crud.Store`
- SQLite-backed runtime store and in-memory test store
- Pydantic schemas under `backend/app/schemas`
- modular frontend with `pages`, `hooks`, `services`, `components`, `styles`, and `utils`
- backend pytest coverage for scoring and API behavior
- full-stack shell health check

## Next Priorities

### 1. Data Realism

- Replace synthetic ingestion with replayable fixture datasets.
- Add source metadata normalization and deduplication.
- Introduce windowed baselines rather than whole-history approximations.

### 2. Governance Hardening

- Add operator identity and notes to alert transitions.
- Add authentication and authorization.
- Add explicit threshold-change audit trails.

### 3. Persistence Evolution

- Add a normalized relational schema if query complexity grows beyond JSON blobs in SQLite.
- Add migration tooling if storage shape becomes nontrivial.
- Add background execution support for longer ingest jobs.

### 4. Frontend Depth

- Add alert action controls to the dashboard.
- Add bias diagnostics views to the UI.
- Add frontend test coverage.

### 5. Evaluation

- Add offline evaluation fixtures and metrics.
- Measure alert precision/recall on labeled replay datasets.
- Compare behavior across population tiers and low-sample regions.
