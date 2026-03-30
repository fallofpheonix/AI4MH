# AI4MH Architecture

## Data Flow

```text
Synthetic posts
  -> app/services/ingestion_service.py
  -> app/services/enrichment_service.py
  -> app/services/scoring_service.py
  -> app/services/alert_service.py
  -> app/crud/sqlite.py
  -> app/api/v1/routes/*
  -> frontend/src/services/dashboardService.js
  -> frontend/src/pages/DashboardPage.jsx
```

## Backend Layout

```text
backend/
  app/
    api/
      dependencies.py        FastAPI dependency wiring
      router.py              top-level API router
      v1/
        router.py            v1 router aggregation
        routes/              ingest, monitoring, alert handlers
    core/
      config.py              Pydantic settings and env parsing
      container.py           application service container
      db.py                  store factory and DB wiring
    crud/
      base.py                abstract persistence contract
      memory.py              in-memory test store
      sqlite.py              SQLite-backed store
    schemas/
      post.py                RawPost, EnrichedPost
      score.py               RegionScore
      alert.py               Alert, LogEvent
    services/
      ingestion_service.py   synthetic dataset generation
      enrichment_service.py  sentiment and keyword enrichment
      scoring_service.py     region scoring engine
      alert_service.py       alert lifecycle management
      pipeline_service.py    end-to-end orchestration
    utils/
      population.py          population tier helper
  tests/
    conftest.py
    test_api.py
    test_scoring.py
```

## Frontend Layout

```text
frontend/
  src/
    components/
      common/                small reusable UI primitives
      layout/                app shell composition
      features/              alert and monitoring widgets
    hooks/
      useDashboardData.js    polling, ingest, snapshot state
    pages/
      DashboardPage.jsx      page composition
    services/
      apiClient.js           base HTTP client
      dashboardService.js    dashboard-specific queries
    styles/
      global.css             global theme and layout rules
    utils/
      score.js               score formatting and coloring
```

## API Surface

- Base prefix: `/api`
- Current version: `/v1`
- Effective endpoints: `/api/v1/*`

### Monitoring

- `GET /api/v1/posts?limit=60`
- `GET /api/v1/scores`
- `GET /api/v1/alerts`
- `GET /api/v1/logs?limit=100`
- `GET /api/v1/bias`

### Pipeline Control

- `POST /api/v1/ingest?n=30`

### Alert Lifecycle

- `POST /api/v1/alerts/{id}/ack`
- `POST /api/v1/alerts/{id}/dismiss`
- `POST /api/v1/alerts/{id}/resolve`

## Invariants

- API handlers stay thin; orchestration lives in `services`.
- Persistence depends on the `crud.Store` interface, not on route handlers.
- Domain payloads are defined in `schemas` and reused across services and storage.
- SQLite remains append/update-oriented JSON storage; no ORM layer exists yet.
- Frontend data access is isolated under `src/services`; page state lives in hooks.

## Constraints

- Time complexity per ingest cycle remains dominated by scoring over stored posts: `O(P + R log R)` for posts `P` and scored regions `R`.
- Memory in `MemoryStore` is bounded by `max_posts`.
- `SQLiteStore` serializes writes with a process-local lock and uses WAL mode.
- No auth/security subsystem exists yet; adding one should land in `app/core/security.py` or a dedicated auth package when requirements exist.

## Failure Considerations

- Backend unavailable: frontend shows a transport error banner.
- Enrichment failure: post is dropped, pipeline continues.
- All-bot region: scoring returns `None` for that region.
- Unknown alert transition: API returns HTTP 404.
