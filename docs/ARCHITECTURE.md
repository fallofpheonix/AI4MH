# AI4MH Architecture

## High-Level Data Flow

```text
Synthetic or replayed posts
  -> NLP enrichment          (pipeline/enrich.py)
  -> region grouping         (pipeline/aggregate.py)
  -> crisis scoring          (pipeline/score.py)
  -> confidence estimation   (pipeline/score.py)
  -> escalation gate         (pipeline/score.py)
  -> alert generation        (pipeline/alert.py)
  -> alerts, logs, API       (main.py)
  -> frontend monitor        (frontend/src/App.jsx)
```

## Backend Structure

```
backend/
    config.py              # Pydantic Settings — all tunable constants
    main.py                # FastAPI routes only; delegates to pipeline/storage
    pipeline/
        ingest.py          # Synthetic post generation
        enrich.py          # VADER sentiment + crisis keyword detection
        aggregate.py       # Region grouping and global baseline
        score.py           # Crisis scoring engine
        alert.py           # Alert generation and lifecycle transitions
    storage/
        base.py            # Abstract Store interface
        memory.py          # In-memory Store implementation
        sqlite.py          # Persistent SQLite Store implementation (WAL mode)
    models/
        post.py            # RawPost, EnrichedPost
        score.py           # RegionScore
        alert.py           # Alert, LogEvent
    evaluation/
        metrics.py         # Precision, recall, F1, FPR
    lexicons/
        crisis_terms_v1.json  # Crisis keyword list
    tests/
        conftest.py        # Shared pytest fixtures
        test_scoring.py    # Unit tests for scoring functions
        test_api.py        # Integration tests for API endpoints
```

## Module Responsibilities

### `config.py`

- Pydantic `Settings` class with `AI4MH_` env-var prefix.
- Holds `ALERT_THRESHOLD`, `MAX_POSTS`, `WEIGHTS`, `ESCALATION_THRESHOLDS`,
  and `CRISIS_TERMS` (loaded from the lexicon file).
- All pipeline modules import `settings` from here.

### `main.py`

- FastAPI entrypoint — routes only, no pipeline logic.
- Instantiates one `Store` (default: `SQLiteStore`) for the process lifetime.
- Delegates all work to pipeline functions and the store.
- Alert lifecycle endpoints: `POST /api/alerts/{id}/ack|dismiss|resolve`.

### `pipeline/ingest.py`

- `generate_post()` → single synthetic `RawPost`.
- `generate_dataset(n)` → list of `RawPost` objects.
- Swap with a real PRAW call for production.

### `pipeline/enrich.py`

- `enrich_post(post)` → `EnrichedPost` with VADER sentiment and keyword flags.
- `enrich_batch(posts)` → list of `EnrichedPost`; skips erroring posts.

### `pipeline/aggregate.py`

- `group_by_region(posts)` → `{region_id: [EnrichedPost]}`.
- `compute_global_avg(groups)` → mean posts-per-region baseline.

### `pipeline/score.py`

- Signal functions: `_sentiment_intensity`, `_volume_spike`,
  `_geo_cluster`, `_trend_acceleration`, `_confidence`.
- `score_region(region_id, posts, global_avg)` → `RegionScore | None`.
- `score_all_regions(posts, affected_regions, existing_scores)` →
  sorted list of `RegionScore`; supports partial region updates.

### `pipeline/alert.py`

- `generate_alerts(scores, existing_alerts, region_posts)` →
  `(alerts, log_events)`.
- Preserves lifecycle state (`acknowledged`, `dismissed`, `resolved`)
  across ingest cycles.

### `storage/base.py`

- Abstract `Store` interface: `save_posts`, `get_posts`, `save_scores`,
  `get_scores`, `save_alerts`, `get_alerts`, `get_alert`, `update_alert`,
  `append_log`, `get_logs`.

### `storage/memory.py`

- Thread-safe in-memory implementation of `Store`.
- Replace with Redis or SQLite by implementing the same interface.

### `models/`

- `RawPost`, `EnrichedPost` — post lifecycle.
- `RegionScore` — crisis score snapshot per region.
- `Alert` — lifecycle-managed alert with evidence and scoring breakdown.
- `LogEvent` — append-only log entry.

### `evaluation/metrics.py`

- `compute_classification_metrics(posts)` → dict with `tp`, `fp`, `fn`,
  `tn`, `precision`, `recall`, `f1`, `fpr`.

## Alert Lifecycle

```
review_required  →  acknowledged  →  resolved
                 →  dismissed
```

State transitions are recorded in the append-only log.

## API Contract

### `POST /api/ingest?n=30`

Runs one pipeline cycle for *n* new posts.
Returns `total_posts`, `regions_scored`, `alerts`.

### `GET /api/posts?limit=60`

Returns recent enriched posts.

### `GET /api/scores`

Returns current region score snapshots, sorted by crisis_score descending.

### `GET /api/alerts`

Returns the current alert list with lifecycle state.

### `POST /api/alerts/{id}/ack`
### `POST /api/alerts/{id}/dismiss`
### `POST /api/alerts/{id}/resolve`

Lifecycle transitions for a specific alert.

### `GET /api/logs?limit=100`

Returns recent append-only log events.

### `GET /api/bias`

Returns population-tier and per-region diagnostics for skew monitoring.

## Configuration

All constants are tunable via environment variables with the `AI4MH_` prefix:

| Variable                    | Default | Description                           |
|-----------------------------|---------|---------------------------------------|
| `AI4MH_ALERT_THRESHOLD`     | 0.75    | Minimum crisis_score for an alert     |
| `AI4MH_MAX_POSTS`           | 500     | Post cap in the in-memory store       |

Weights and escalation thresholds are set in `config.py` and can be
overridden by providing JSON-encoded values via the matching env variables.

## Performance Characteristics

- Partial region updates: only affected regions are rescored after each
  ingest, reducing work from O(all regions × posts) to O(new regions × posts).
- In-memory storage is capped at `MAX_POSTS` (default 500).
- Thread safety is enforced via a `threading.Lock` in `MemoryStore`.

## Failure Model

- Backend unavailable: frontend shows connection error.
- Sparse data: score exists with low confidence; bias endpoint exposes this.
- High bot ratio: confidence drops and escalation becomes less likely.
- Enrichment failures: post is skipped and an error is logged; pipeline continues.
