# AI4MH Roadmap

## Current State

Implemented:

- synthetic ingestion,
- NLP enrichment (VADER + crisis keywords),
- regional scoring (sentiment, volume, geo cluster, trend),
- confidence and threshold gating,
- alert lifecycle management (review_required → acknowledged/dismissed/resolved),
- alert/log APIs,
- modular pipeline (pipeline/, models/, storage/, evaluation/),
- Pydantic Settings configuration system,
- in-memory storage with abstract interface,
- schema validation via Pydantic models,
- partial region score updates (only affected regions rescored per cycle),
- pytest unit and integration test suite,
- single-page monitor,
- local health-check script.

## Next Development Priorities

### Phase 1: Data realism

- Replace synthetic ingestion with replayable dataset loaders.
- Add deduplication and source metadata normalization.
- Introduce realistic time-window baselines.

### Phase 2: Governance hardening

- Make minimum sample thresholds explicit in scoring outputs.
- Add media-spike dampening.
- Add coordinated-activity heuristics.
- Preserve evidence bundles for every generated alert (evidence_post_ids and score_breakdown are stored on each Alert).

### Phase 3: Geospatial quality

- Replace coarse region IDs with county-aligned geographic references.
- Add longitudinal heatmap views and time-window navigation.
- Separate county baselines from global baseline approximation.

### Phase 4: Evaluation

- Add offline evaluation fixtures.
- Measure precision, recall, and false-positive rate for alert generation.
- Add region-tier comparisons for sparse-data bias monitoring.
- Wire `evaluation/metrics.py` into an evaluation API endpoint.

### Phase 5: Operational readiness

- Move from in-memory state to persistent storage (Redis or SQLite).
- Implement Redis/SQLite backends by subclassing `storage.base.Store`.
- Add deployment packaging and environment configuration.
- Add background task support for long-running ingestion cycles.

## Development Rules

- Preserve deterministic behavior unless explicitly changing a scoring assumption.
- Avoid adding framework weight where a configuration file is sufficient.
- Keep human review as the terminal automated action.
- Pipeline modules must not import FastAPI.
- Update this roadmap, the spec, and the architecture doc before adding major features.
