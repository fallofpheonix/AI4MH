# SPEC

## Problem

- Public-health reporting is delayed.
- Online discussion signals appear earlier but are noisy, sparse, and manipulable.
- The system must decide whether regional distress signals are credible enough for human review.

## Goal

- Generate explainable regional crisis indicators from discussion-like posts.
- Escalate only to human review, never directly to intervention.

## Inputs

- Synthetic raw posts with:
  - text
  - subreddit
  - region ID / region name
  - timestamp
  - engagement counts
  - bot flag
  - ground-truth crisis label
- Environment configuration via `AI4MH_*`

## Outputs

- enriched posts
- region scores
- active alerts
- append-only log events
- bias diagnostics
- dashboard snapshot via HTTP API

## In Scope

- ingestion and normalization of synthetic posts
- sentiment and keyword enrichment
- region scoring
- confidence estimation
- threshold-based alert generation
- alert lifecycle transitions
- append-only logging
- minimal monitoring dashboard
- SQLite-backed persistence through a store abstraction

## Out Of Scope

- live social platform ingestion
- user accounts, auth, RBAC
- automatic intervention workflows
- advanced ML training/inference stack
- distributed processing

## Success Metrics

- `/api/v1/ingest` returns operational summary
- `/api/v1/scores` returns ranked region scores
- `/api/v1/alerts` exposes current alert state
- `/api/v1/bias` exposes tier and low-sample diagnostics
- backend pytest passes
- frontend production build passes
- full-stack health check passes
