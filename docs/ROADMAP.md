# AI4MH Roadmap

## Current State

Implemented:

- synthetic ingestion,
- NLP enrichment,
- regional scoring,
- confidence and threshold gating,
- alert/log APIs,
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
- Preserve evidence bundles for every generated alert.

### Phase 3: Geospatial quality

- Replace coarse region IDs with county-aligned geographic references.
- Add longitudinal heatmap views and time-window navigation.
- Separate county baselines from global baseline approximation.

### Phase 4: Evaluation

- Add offline evaluation fixtures.
- Measure precision, recall, and false-positive rate for alert generation.
- Add region-tier comparisons for sparse-data bias monitoring.

### Phase 5: Operational readiness

- Move from in-memory state to persistent storage.
- Add config-driven thresholds and lexicons.
- Add deployment packaging and environment configuration.

## Development Rules

- Preserve deterministic behavior unless explicitly changing a scoring assumption.
- Avoid adding framework weight where a configuration file is sufficient.
- Keep human review as the terminal automated action.
- Update this roadmap, the spec, and the architecture doc before adding major features.
