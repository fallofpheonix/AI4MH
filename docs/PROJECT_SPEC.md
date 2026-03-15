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
- append-only event logging,
- minimal monitoring dashboard.

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

## Success Criteria

- Regional scores are generated for active regions.
- Alerts only appear when threshold conditions are met.
- Bias diagnostics expose low-sample and population-tier skew.
- The stack runs locally with the provided health check.
