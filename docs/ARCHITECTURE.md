# AI4MH Architecture

## High-Level Data Flow

```text
Synthetic or replayed posts
  -> NLP enrichment
  -> region grouping
  -> crisis scoring
  -> confidence estimation
  -> escalation gate
  -> alerts, logs, diagnostics
  -> frontend monitor
```

## Backend Modules

### `backend/main.py`

- FastAPI entrypoint.
- Holds in-memory state for posts, scores, alerts, and logs.
- Exposes `/api/posts`, `/api/scores`, `/api/alerts`, `/api/logs`, `/api/bias`, `/api/ingest`.

### `backend/ingest_posts.py`

- Generates replayable synthetic posts.
- Defines region metadata and synthetic crisis/non-crisis text pools.

### `backend/nlp_processing.py`

- Computes VADER sentiment.
- Matches crisis terms.
- Adds `nlp_crisis_flag`, `ground_truth_crisis`, and `ai_correct`.

### `backend/crisis_scoring.py`

- Groups posts by region.
- Computes signal components:
  - `sentiment_intensity`
  - `volume_spike`
  - `geo_cluster`
  - `trend_accel`
- Computes `crisis_score`, `confidence`, and `should_escalate`.

## Frontend

### `frontend/src/App.jsx`

- Fetches posts, scores, alerts, and logs.
- Supports manual ingest and optional 5-second live ingest mode.
- Shows a minimal operator view for current pipeline state.

## API Contract

### `POST /api/ingest?n=30`

- Runs one refresh cycle.
- Returns post count, region count, and alert count.

### `GET /api/posts?limit=60`

- Returns recent enriched posts.

### `GET /api/scores`

- Returns current region score snapshots.

### `GET /api/alerts`

- Returns current `review_required` alerts.

### `GET /api/logs?limit=100`

- Returns recent append-only events.

### `GET /api/bias`

- Returns population-tier and per-region diagnostics for skew monitoring.

## Performance Characteristics

- Regional scoring is `O(n)` in the number of posts in memory.
- In-memory storage is capped at 500 posts in the current implementation.
- Frontend polling cost is bounded by a small set of lightweight JSON endpoints.

## Failure Model

- Backend unavailable: frontend shows connection error.
- Sparse data: score may exist with low confidence; bias endpoint exposes this.
- High bot ratio: confidence drops and escalation becomes less likely.
