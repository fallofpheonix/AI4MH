# Architecture

## Runtime Flow

```text
Synthetic post generation
  -> enrichment (sentiment + keyword match)
  -> regional scoring
  -> alert rebuild
  -> SQLite persistence
  -> FastAPI endpoints
  -> React dashboard
```

## Backend Structure

- `backend/app/main.py`
  Creates the FastAPI app, wires CORS, initializes the application container, and bootstraps the pipeline on startup.
- `backend/app/api/`
  HTTP routing and dependency access.
- `backend/app/core/`
  Settings, container, and storage wiring.
- `backend/app/crud/`
  Store abstraction and SQLite implementation.
- `backend/app/schemas/`
  Pydantic models for posts, scores, alerts, and logs.
- `backend/app/services/`
  Ingestion, enrichment, scoring, alerting, and pipeline orchestration.
- `backend/app/utils/`
  Small shared helpers.

## Data Model

### Posts

`RawPost` represents synthetic source events.

`EnrichedPost` adds:

- `sentiment`
- `keyword_count`
- `keyword_terms`
- `nlp_crisis_flag`
- `ai_correct`

### Scores

`RegionScore` includes:

- traffic counts
- bot ratio
- component scores
- aggregate `crisis_score`
- `confidence`
- `should_escalate`

### Alerts

Alerts store:

- `region`
- `score`
- `status`
- `confidence`
- `sample_size`
- `score_breakdown`
- `evidence_post_ids`

## Storage

SQLite tables:

- `posts`
- `scores`
- `alerts`
- `logs`

The shipped backend uses SQLite by default through `create_store()`.

## Operational Constraints

- Input is synthetic and non-replayable across runs.
- Bootstrapping seeds the store on first startup.
- Alert transitions are explicit API calls.
- Dashboard polling can continuously trigger new ingestion cycles.

## Current Gaps

- No auth or multi-user controls
- No production database migration layer
- No live ingestion connectors
- No frontend automated test suite
