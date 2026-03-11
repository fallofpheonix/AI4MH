# AI4MH - GSoC Contributor Selection Submission

Project: AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis  
Scenario: within 72 hours, three Alabama counties show rising negative sentiment and suicide-related language; system must determine whether escalation to human review is warranted.

## 1. System Overview

### Objective
Design a governance-ready crisis signal pipeline for early warning support in public-health settings. The system detects regional crisis signals and determines whether human review is required.

### Pipeline
```text
Data Ingestion -> NLP Enrichment -> Regional Signal Aggregation -> Crisis Scoring
-> Confidence Estimation -> Escalation Decision -> Human Review Queue -> Audit Logs
```

### Inputs
- Social-style text posts
- Timestamp
- Region metadata
- User metadata (including bot-like indicators in synthetic data)

### Outputs
- `crisis_score` by region
- `confidence` by region
- `review_required` alerts
- append-only event logs

### Implemented Components
- Backend API: `backend/main.py`
- NLP module: `backend/nlp_processing.py`
- Scoring module: `backend/crisis_scoring.py`
- Frontend monitor: `frontend/src/App.jsx`

## 2. Crisis Signal Design (Core Component)

### Signals Used
1. Sentiment intensity
2. Volume spike detection
3. Geographic clustering  
4. Trend acceleration (implementation extension)

### Scoring Formulation
```text
crisis_score =
  0.35 * sentiment_intensity +
  0.30 * volume_spike +
  0.20 * geo_cluster +
  0.15 * trend_accel
```

### Minimum Sample Size and Stabilization
- Region scoring enforces minimum effective sample rules in code path.
- Volume and confidence factors are bounded to reduce unstable spikes.

### Confidence / Uncertainty
Confidence is computed from:
- sample volume factor
- consistency factor (bot ratio penalty)
- coverage factor  
and is returned for every region.

### Escalation Threshold
```text
if crisis_score > 0.75:
    review_required
```

Implemented in:
- `backend/crisis_scoring.py`
- `backend/main.py`

## 3. Governance & Risk Controls

### Bot Amplification / Coordinated Activity
- Bot-like posts are marked in ingestion and penalized in scoring confidence.
- Bot ratio is tracked in region outputs.
- High-risk alerts are not auto-acted; they are routed to human review.

### Media-Driven Spikes
- Current MVP uses bounded spike scoring and confidence controls to limit raw burst impact.
- Governance interpretation is deferred to human review on high scores.

### Rural Underrepresentation / Sparse Data
- Confidence scales with available sample and coverage.
- Low-sample patterns are exposed in diagnostics endpoint for monitoring.

### Escalation and Human-in-the-Loop
- Escalation is threshold-based (`score > 0.75`).
- Alert status is `review_required`; no automated intervention is executed.

### Audit Logging Structure
Each decision event is logged with:
- timestamp
- event type
- region
- score
- confidence
- sample size

API surface for governance evidence:
- `GET /api/alerts`
- `GET /api/logs`
- `GET /api/bias`

## 4. Governance Reflection (Short Section)

### Primary Risk of Premature Deployment
False positive crisis escalation from noisy or manipulated social signals can misallocate limited public-health resources and reduce trust in the monitoring system.

### Single Most Important Safeguard
Mandatory human verification before any operational escalation decision.

## Generative AI Use Disclosure

Generative AI tooling was used to assist drafting documentation structure, editing language, and accelerating implementation scaffolding. Final technical decisions, thresholds, and code verification were manually reviewed and validated through executable health checks.

## Reproducibility (Implementation Check)

Run:
```bash
./scripts/full_health_check.sh
```

Expected result:
```text
PASS: full health check completed
```
