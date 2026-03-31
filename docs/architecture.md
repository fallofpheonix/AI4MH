# Architecture

## Overview

AI4MH is structured as a six-stage pipeline that runs on every ingest cycle:

```text
1. Synthetic post generation  (IngestionService)
     -> 2. Enrichment               (EnrichmentService)
          -> 3. Regional scoring    (ScoringService)
               -> 4. Alert rebuild  (AlertService)
                    -> 5. Persistence (SQLiteStore)
                         -> 6. HTTP API (FastAPI + React dashboard)
```

On first startup the pipeline bootstraps a seed batch of synthetic posts so the dashboard has data immediately.

## Backend Structure

```text
backend/app/
  main.py          Entry point — creates the FastAPI app, registers CORS,
                   wires the ApplicationContainer, and runs bootstrap on startup.
  api/
    router.py      Top-level APIRouter; mounts the v1 sub-router under /v1.
    v1/
      router.py    Aggregates alerts, ingest, and monitoring routers.
      routes/
        alerts.py     POST /alerts/{id}/ack|dismiss|resolve
        ingest.py     POST /ingest
        monitoring.py GET /posts|scores|alerts|logs|bias
    dependencies.py  FastAPI Depends helper that resolves ApplicationContainer.
  core/
    config.py      Pydantic Settings — reads AI4MH_* env vars and .env file.
    container.py   ApplicationContainer dataclass holding pipeline + alerts refs.
    db.py          create_store() factory that returns a SQLiteStore instance.
  crud/
    base.py        Abstract Store interface (save/get for posts, scores, alerts, logs).
    sqlite.py      SQLiteStore — concrete WAL-mode SQLite implementation.
  schemas/
    post.py        RawPost and EnrichedPost Pydantic models.
    score.py       RegionScore Pydantic model.
    alert.py       Alert and LogEvent Pydantic models.
  services/
    ingestion_service.py   Synthetic post generator.
    enrichment_service.py  VADER sentiment + crisis keyword matching.
    scoring_service.py     Weighted crisis score formula per region.
    alert_service.py       Alert lifecycle management.
    pipeline_service.py    Orchestrates the full ingest cycle.
  fixtures/
    synthetic_posts.py  REGIONS, CRISIS_TEXTS, NORMAL_TEXTS, SUBREDDITS lists.
    crisis_terms_v1.json Bundled crisis keyword lexicon (fallback).
  utils/
    population.py   classify_population_tier() — rural / suburban / urban.
```

## Pipeline Stages

### 1. Ingestion

`IngestionService.build_dataset(size)` generates `size` synthetic `RawPost` objects.
Each post is randomly assigned a region, subreddit, and text drawn from
`CRISIS_TEXTS` (~25 % probability) or `NORMAL_TEXTS` (~75 % probability).
~7 % of posts are flagged as bots.

### 2. Enrichment

`EnrichmentService.enrich_post(post)` adds:

- **`sentiment`** — VADER compound score in [-1.0, 1.0].
- **`keyword_terms`** — crisis terms from `crisis_terms_v1.json` found in the post text.
- **`keyword_count`** — number of matched terms.
- **`nlp_crisis_flag`** — `True` when `sentiment < -0.4` **or** any keyword is matched.
- **`ai_correct`** — `True` when `nlp_crisis_flag` matches `ground_truth_crisis`.

### 3. Scoring

`ScoringService.score_region(region_id, posts, global_average)` computes four
normalised component scores (each in [0, 1]), then blends them with configurable
weights (sum must equal 1.0):

| Component | Default weight | Description |
|---|---|---|
| `sentiment_intensity` | 0.35 | Fraction of posts with sentiment < -0.2 |
| `volume_spike` | 0.30 | Post count relative to 60 % of global average |
| `geo_cluster` | 0.20 | Fraction of posts flagged by NLP |
| `trend_accel` | 0.15 | Difference in crisis rate between older and newer half |

```
crisis_score = 0.35 × sentiment_intensity
             + 0.30 × volume_spike
             + 0.20 × geo_cluster
             + 0.15 × trend_accel
```

A region produces an alert candidate when all four conditions are satisfied:

- `crisis_score >= 0.70`
- `confidence >= 0.60`
- `post_count >= 10` (clean posts only)
- `bot_ratio < 0.25`

**Confidence** is a composite of volume coverage, bot-ratio penalty, and post count:

```
confidence = min(post_count / 200, 1) × (1 - min(bot_ratio × 2, 1)) × min(post_count / 50, 1)
```

Weights and thresholds are configurable via environment variables (see `AI4MH_WEIGHTS` and `AI4MH_ESCALATION_THRESHOLDS` in `config.py`).

### 4. Alert Rebuild

`AlertService.rebuild_alerts(scores, region_posts)` runs after every scoring cycle:

- Regions that `should_escalate` and have **no existing alert** → create a new `Alert` with status `review_required`.
- Regions that `should_escalate` and have an **existing alert** → update score/confidence/evidence fields only.
- Regions that **no longer** escalate → their `review_required` alerts are dropped; alerts with other statuses are preserved.

Alert status transitions are triggered by explicit API calls:

```text
review_required → acknowledged → resolved
review_required → dismissed
```

Each transition is logged as a `LogEvent`.

### 5. Persistence

`SQLiteStore` persists all state in a single WAL-mode SQLite file (`ai4mh.db` by default).

Tables:

| Table | Key | Content |
|---|---|---|
| `posts` | `id` (TEXT) | JSON-serialised `EnrichedPost`, plus integer `idx` for recency ordering |
| `scores` | `region_id` (TEXT) | JSON-serialised `RegionScore` (full replace on each cycle) |
| `alerts` | `id` (TEXT UUID) | JSON-serialised `Alert` (full replace on each cycle) |
| `logs` | autoincrement `id` | JSON-serialised `LogEvent` |

The store trims the posts table to `max_posts` (default 500) on every write.

## Data Models

### RawPost

Synthetic source event — region, subreddit, text, engagement counters, and ground-truth crisis label.

### EnrichedPost

Extends `RawPost` with VADER sentiment, keyword matches, NLP crisis flag, and correctness flag.

### RegionScore

Per-region aggregate: post count, bot stats, four component scores, composite `crisis_score`, `confidence`, and `should_escalate` flag.

### Alert

Persistent alert record with UUID, region, score, status, confidence, sample size, score breakdown, and evidence post IDs.

### LogEvent

Timestamped event with a string key and a free-form JSON payload. Used for `ingest_completed` and `alert_*` events.

## Frontend

The React/Vite dashboard (`frontend/src`) polls the backend API on a configurable interval.

Key files:

| File | Role |
|---|---|
| `src/services/apiClient.js` | Thin `fetch` wrapper; reads `VITE_API_BASE_URL` env var |
| `src/services/dashboardService.js` | Parallel-fetches posts, scores, alerts, and logs |
| `src/hooks/useDashboardData.js` | State management and live-polling hook |
| `src/pages/DashboardPage.jsx` | Top-level page composing alerts, posts, logs, and metrics |

## Operational Constraints

- Input is synthetic and non-replayable across runs.
- Bootstrapping seeds the store on first startup only.
- Alert transitions require explicit API calls; there is no automated resolution.
- Dashboard live mode triggers a new ingest cycle every 5 seconds.

## Current Gaps

- No auth or multi-user controls
- No production database migration layer
- No live ingestion connectors
- No frontend automated test suite
- Scoring weights are fixed per settings instance; runtime reconfiguration requires restart
