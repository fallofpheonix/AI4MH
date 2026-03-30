# ARCH

## Top-Level Layout

```text
backend/app/
  api/        HTTP routing and dependency wiring
  core/       config, container, store factory
  crud/       persistence contracts and implementations
  schemas/    typed payload models
  services/   domain logic and orchestration
  utils/      shared helper logic

frontend/src/
  components/ UI primitives and feature widgets
  hooks/      stateful orchestration
  pages/      page composition
  services/   HTTP client and data fetchers
  styles/     global UI styling
  utils/      UI helpers
```

## Data Flow

```text
RawPost
  -> EnrichmentService.enrich_batch
  -> EnrichedPost
  -> ScoringService.score_regions
  -> RegionScore
  -> AlertService.rebuild_alerts
  -> Alert / LogEvent
  -> Store (SQLite or Memory)
  -> FastAPI /api/v1 routes
  -> dashboardService.js
  -> useDashboardData.js
  -> DashboardPage.jsx
```

## Backend Interfaces

- `ApplicationContainer`
  - `pipeline: PipelineService`
  - `alerts: AlertService`
- `Store`
  - posts, scores, alerts, logs CRUD-like methods
- `PipelineService`
  - `bootstrap`
  - `run_cycle`
  - `list_posts`
  - `list_scores`
  - `list_logs`
  - `build_bias_summary`

## Frontend Interfaces

- `apiClient.js`
  - `getJson(path)`
  - `postJson(path)`
- `dashboardService.js`
  - `fetchDashboardSnapshot()`
  - `ingestPosts(batchSize)`
- `useDashboardData`
  - owns polling, ingest trigger, local UI state

## External Dependencies

- FastAPI
- Pydantic / pydantic-settings
- SQLite
- vaderSentiment
- React
- Vite
