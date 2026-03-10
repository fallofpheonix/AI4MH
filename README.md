# AI4MH (AI for Mental Health Crisis Monitoring)

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis.

Google Summer of Code 2026 - Contributor Selection Task  
Organization: Institute for Social Science Research (ISSR), The University of Alabama  
Mentor: David M. White, MPH, MPA  
Contact: dmwhite@ua.edu

## 1. Repository Purpose

This repository delivers a working minimum prototype for AI4MH governance readiness:

- end-to-end crisis signal pipeline
- explicit governance controls
- human-in-the-loop review workflow
- auditable decision logging
- exportable data for analysis

This is a systems-design implementation, not a model-competition submission.

## 2. What Works Now

Implemented and runnable:

1. Synthetic social post ingestion across multiple regions
2. NLP enrichment (VADER sentiment + crisis lexicon)
3. Regional crisis scoring engine
4. Governance controls:
   - bot-risk handling
   - coordinated-activity detection
   - media-amplification dampening
   - sparse-region confidence handling
5. Escalation policy (`NO_ACTION`, `MONITOR`, `HUMAN_REVIEW_REQUIRED`)
6. Human review queue simulation
7. Append-only audit decision logs
8. API exports in JSON and CSV
9. React dashboard connected live to backend API

## 3. System Architecture

```text
Data Ingestion -> NLP Enrichment -> Signal Aggregation -> Crisis Scoring
      -> Governance Controls -> Escalation Decision -> Human Review Queue
      -> Audit Log + Dashboard + Export APIs
```

Core signal model:

```text
crisis_score = 0.4*sentiment_intensity + 0.4*volume_score + 0.2*geo_cluster
smoothed_score = alpha*crisis_score + (1-alpha)*previous_score
```

Escalation policy:

```text
if crisis_score > 0.75 and confidence > 0.6:
    HUMAN_REVIEW_REQUIRED
elif crisis_score > 0.4:
    MONITOR
else:
    NO_ACTION
```

## 4. Governance and Risk Controls

Implemented governance checks:

1. Bot activity scoring (`bot_probability` in `[0,1]`), influence reduction if `> 0.7`
2. Coordinated activity detection (hashtags/text/time synchronization), influence cap
3. Media amplification detection (`media_ratio`), score discount if high
4. Sparse-region policy (time-window extension marker + confidence reduction)
5. Human-in-the-loop routing for high-risk signals only
6. Structured append-only decision logs

## 5. Data Contracts

### Input Post Shape

```json
{
  "text": "I feel completely hopeless",
  "timestamp": "2026-03-11T00:00:00Z",
  "region": "AL-JEF",
  "user_id": "u123",
  "sentiment_score": -0.82
}
```

### Crisis Signal Output

```json
{
  "status": "ok",
  "crisis_score": 0.79,
  "confidence_score": 0.64,
  "escalation_flag": true,
  "human_review_required": true
}
```

### Governance Decision Log Record

```json
{
  "timestamp": "2026-03-11T00:00:00Z",
  "region": "AL-JEF",
  "crisis_score": 0.79,
  "confidence": 0.64,
  "sample_size": 86,
  "decision": "HUMAN_REVIEW_REQUIRED",
  "bot_probability": 0.21,
  "coordinated_activity": false,
  "reviewer_id": null
}
```

## 6. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/posts?limit=60` | Latest NLP-enriched posts |
| GET | `/api/scores` | Regional scores |
| GET | `/api/alerts` | Alert queue |
| POST | `/api/alerts/{id}/review` | Analyst review action |
| GET | `/api/audit` | Audit log |
| POST | `/api/ingest?n=30` | Trigger ingestion |
| GET | `/api/export/json?kind=posts|scores|alerts|audit` | Structured export |
| GET | `/api/export/csv?kind=posts|scores|alerts|audit` | CSV export |

Calibration-support fields in posts:

- `ground_truth_crisis`
- `ai_correct`

## 7. Quick Start

Prerequisites:

- Python `3.12`
- Node.js `18+`

### Backend

```bash
cd backend
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

- `http://127.0.0.1:5173`
- `http://127.0.0.1:8000/api/scores`

### One-Command Full Health Check

```bash
./scripts/full_health_check.sh
```

Validation-only (if services already running):

```bash
./scripts/full_health_check.sh --no-start
```

## 8. Repository Structure

```text
backend/
  main.py
  ingest_posts.py
  nlp_processing.py
  crisis_scoring.py
  crisis_signal_engine.py
  governance_filters.py
  governance_engine.py
  alert_engine.py
  requirements.txt

frontend/
  src/App.jsx
  src/main.jsx
  package.json
  vite.config.js

docs/
  GSOC_submission_template.md
  mentor_rejection_checklist.md

scripts/
  full_health_check.sh
```

## 9. Deliverable Mapping (Task Compliance)

| Required deliverable | Implemented in repo |
|---|---|
| Crisis signal design with sentiment/volume/geo | `backend/crisis_signal_engine.py` + `backend/crisis_scoring.py` |
| Minimum sample-size + smoothing + confidence | `backend/crisis_signal_engine.py` |
| Governance and risk controls | `backend/governance_engine.py` + `backend/governance_filters.py` |
| Escalation thresholds + human-in-loop | `backend/governance_engine.py` + `backend/alert_engine.py` |
| Audit logging structure | `backend/alert_engine.py` + `backend/governance_engine.py` |
| Interactive monitoring dashboard | `frontend/src/App.jsx` |
| Exportable datasets | `/api/export/json`, `/api/export/csv` |
| Submission documentation support | `docs/GSOC_submission_template.md`, `docs/mentor_rejection_checklist.md` |

## 10. Known Scope Limits (Intentional for MVP)

1. In-memory storage only (no persistent DB)
2. Synthetic ingestion source (no live platform APIs)
3. Heuristic governance signals (no advanced classifier)
4. Prototype workflow; not production-deployed infrastructure

## 11. Submission Support Files

- [3-4 Page Submission Template](docs/GSOC_submission_template.md)
- [Mentor Rejection Checklist](docs/mentor_rejection_checklist.md)

