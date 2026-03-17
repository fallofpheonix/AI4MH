# AI4MH Project Specification

## Purpose

AI4MH provides early-warning decision support for public-health teams by converting online discussion signals into regional crisis indicators. The system is designed to answer one operational question: whether a regional shift in distress-related discussion is credible enough to warrant human review.

## Problem

Traditional public-health reporting channels are delayed. Social discussion data appears earlier but is noisy, manipulable, geographically uneven, and operationally unsafe without governance controls.

## Scope

Included:

- post ingestion and normalization,
- NLP enrichment for sentiment and crisis terms,
- region-level aggregation,
- crisis scoring and confidence estimation,
- threshold-based escalation to human review,
- alert lifecycle management (review_required → acknowledged/dismissed/resolved),
- append-only event logging,
- minimal monitoring dashboard,
- configuration system with environment-variable overrides,
- schema validation for all pipeline models,
- storage abstraction (SQLite persistent store by default).

Excluded:

- direct connection to production social APIs,
- persistent database storage,
- automated intervention workflows,
- advanced end-to-end model training,
- user authentication and role management.

## Required Signals

The scoring layer must include:

1. sentiment intensity,
2. volume spike detection,
3. geographic clustering.

The current implementation also includes trend acceleration as a secondary signal.

## Operational Constraints

- Sparse regions must not produce unstable alerts.
- Manipulated traffic must not dominate scoring.
- Public outputs must remain explainable.
- Human review is mandatory before any operational escalation.

## System Invariants

- `review_required` is the highest automated state.
- `crisis_score` without `confidence` is invalid output.
- Logs must preserve timestamp, event type, and payload.
- Score computation must be deterministic for a fixed input set.
- Pipeline modules must not import FastAPI.
- All scoring weights must sum to 1.0 (validated at startup).

## Configuration

All tuneable constants live in `backend/config.py` as a Pydantic `Settings` object.
Values can be overridden via environment variables with the `AI4MH_` prefix.
Weights are validated to sum to 1.0; the crisis-term lexicon is loaded from
`backend/lexicons/crisis_terms_v1.json`.

## Alert Lifecycle

```
review_required  →  acknowledged  →  resolved
                 →  dismissed
```

Each transition is recorded in the append-only log and the alert record
preserves evidence post IDs and the scoring breakdown that triggered it.

## Success Criteria

- Regional scores are generated for active regions.
- Alerts only appear when threshold conditions are met.
- Alert lifecycle transitions are exposed via dedicated API endpoints.
- Bias diagnostics expose low-sample and population-tier skew.
- The stack runs locally with the provided health check.
- Unit and integration test suite passes without failures.
