# AI4MH - Direct Answer (Contributor Selection Task)

## Evaluator-First Summary

This repository satisfies the three required deliverables with runnable code and explicit governance logic:

1. Crisis Signal Design
2. Governance & Risk Controls
3. Governance Reflection

## Problem
AI4MH must determine whether rising crisis-related social signals across Alabama counties are credible enough to escalate to human review.

## Scenario
Within 72 hours, three counties show increased negative sentiment and suicide-related language. The system must decide if escalation is warranted.

## Deliverable 1: Crisis Signal Design (Core Component)
Implemented in:
- `backend/crisis_signal_engine.py`
- `backend/crisis_scoring.py`

Implemented logic:
- Signals: sentiment intensity, volume spike, geographic clustering
- Minimum sample-size gate (`MIN_SAMPLE_SIZE`)
- Stabilization (EMA)
- Confidence estimate from sample size, geo coverage, sentiment variance
- Escalation threshold logic

Core form:
```text
crisis_score = 0.4*sentiment + 0.4*volume_spike + 0.2*geo_cluster
smoothed_score = alpha*current + (1-alpha)*previous
```

## Deliverable 2: Governance & Risk Controls
Implemented in:
- `backend/governance_engine.py`
- `backend/governance_filters.py`
- `backend/alert_engine.py`

Implemented controls:
- Bot amplification detection (`bot_probability`) + influence reduction
- Coordinated activity detection + influence cap
- Media-driven spike detection (`media_ratio`) + score dampening
- Sparse/rural handling (confidence reduction + window extension marker)
- Human-in-the-loop routing (`HUMAN_REVIEW_REQUIRED`)
- Structured append-only audit logging

Escalation policy:
```text
if crisis_score > 0.75 and confidence > 0.6: HUMAN_REVIEW_REQUIRED
elif crisis_score > 0.4: MONITOR
else: NO_ACTION
```

## Deliverable 3: Governance Reflection (Short)
- Primary risk of premature deployment: false crisis escalation from noisy/manipulated social signals, causing misallocation of public resources and trust harm.
- Most important safeguard: mandatory human verification before any operational escalation.

## Evaluation Criteria Mapping (What Evaluators Need)

1. Systems thinking and architectural clarity
- End-to-end pipeline is implemented (`backend/main.py` + scoring/governance modules + frontend).
- Inputs, processing, outputs, escalation, and audit are explicit.

2. Responsible AI and governance awareness
- Human-in-the-loop escalation only (`HUMAN_REVIEW_REQUIRED`).
- Governance checks for bot/coordinated/media risks and sparse regions.
- Structured audit logging is present.

3. Bias identification and mitigation strategy
- Sparse-region handling reduces overconfidence under low coverage.
- Manipulation controls reduce inflated signals.

4. Treatment of uncertainty and confidence modeling
- Confidence score is computed and required for escalation.
- Minimum sample-size and stabilization guard against unstable spikes.

5. Professional written communication
- Deliverables mapped directly to files and executable checks.

## Working Prototype
Backend + frontend are connected and runnable.

Backend API (`backend/main.py`):
- `GET /api/posts?limit=60`
- `GET /api/scores`
- `GET /api/alerts`
- `POST /api/alerts/{id}/review`
- `GET /api/audit`
- `POST /api/ingest?n=30`
- `GET /api/export/json?kind=posts|scores|alerts|audit`
- `GET /api/export/csv?kind=posts|scores|alerts|audit`

Frontend:
- `frontend/src/App.jsx` (dashboard + review flow)

## 2-Minute Evaluator Verification

1. Start services (or use already running ones).
2. Run:
```bash
./scripts/full_health_check.sh --no-start
```
3. Confirm `PASS: full health check completed`.
4. Inspect:
- scoring logic: `backend/crisis_signal_engine.py`
- governance logic: `backend/governance_engine.py`
- API wiring: `backend/main.py`

## PDF Structure Required by Program

Use these section headers in submission PDF:

1. System Overview (+ optional architecture diagram)
2. Crisis Signal Design (Core Component)
3. Governance & Risk Controls
4. Governance Reflection (Short Section)

## Run
```bash
cd backend
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## Verify
```bash
./scripts/full_health_check.sh --no-start
```
