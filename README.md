# AI4MH (AI for Mental Health Crisis Monitoring)

## Problem Statement

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis.

Public health agencies need earlier crisis signals than traditional lagging indicators (hospital admissions, overdose reports, hotline stats). The system must detect rising crisis discourse in near real time and decide whether escalation to human review is warranted.

## Task Context

Google Summer of Code 2026 - Contributor Selection Task  
Organization: Institute for Social Science Research (ISSR), The University of Alabama  
Mentor: David M. White, MPH, MPA

This is a systems/governance task, not a model-building competition.

## Scenario

Within 72 hours, multiple Alabama counties show increased negative sentiment and suicide-related language. The State Behavioral Health Office asks whether this is a credible signal requiring attention.

## Required Deliverables

1. Crisis Signal Design
- Sentiment intensity
- Volume spike detection
- Geographic clustering
- Minimum sample size threshold
- Stabilization/smoothing
- Confidence/uncertainty estimate

2. Governance and Risk Controls
- Bot amplification / coordinated activity handling
- Media-driven spike handling
- Rural sparse-data handling
- Escalation thresholds
- Human-in-the-loop process
- Audit logging structure

3. Governance Reflection (Short Section)
- Identify the primary risk of premature deployment
- Identify the single most important safeguard

## Evaluation Criteria

Submissions are evaluated on:

- Systems thinking and architectural clarity
- Responsible AI and governance awareness
- Bias identification and mitigation strategy
- Treatment of uncertainty and confidence modeling
- Professional written communication

Strong submissions demonstrate constraint discipline, clear logic, and understanding of public-sector responsibility.

## Submission Requirements

- 3-4 pages maximum (excluding optional diagram)
- Optional single architecture diagram
- Clear section headings required
- Submit as a single PDF via the GSoC portal
- Estimated time: 6-8 hours over one week
- Work must be original
- Use of generative AI tools must be disclosed
- Plagiarized or template-based submissions will not be considered

## What This Repository Implements

1. Backend API (FastAPI)
- Ingestion, NLP enrichment, scoring, governance, alerts, audit

2. Frontend Prototype (React)
- Live view of posts, scores, alerts, and review workflow

3. Crisis/Governance Logic
- Crisis scoring engine and governance engine modules

4. Data Export
- JSON and CSV exports for analysis

## Core Decision Logic

```text
crisis_score = 0.4*sentiment + 0.4*volume_spike + 0.2*geo_cluster
smoothed_score = alpha*current + (1-alpha)*previous

if crisis_score > 0.75 and confidence > 0.6:
    HUMAN_REVIEW_REQUIRED
elif crisis_score > 0.4:
    MONITOR
else:
    NO_ACTION
```

## API Endpoints

- `GET /api/posts?limit=60`
- `GET /api/scores`
- `GET /api/alerts`
- `POST /api/alerts/{id}/review`
- `GET /api/audit`
- `POST /api/ingest?n=30`
- `GET /api/export/json?kind=posts|scores|alerts|audit`
- `GET /api/export/csv?kind=posts|scores|alerts|audit`

## Run

Backend:

```bash
cd backend
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:
- `http://127.0.0.1:5173`
- `http://127.0.0.1:8000/api/scores`

## Quick Validation

```bash
./scripts/full_health_check.sh
```

## Supporting Submission Docs

- `docs/GSOC_submission_template.md`
- `docs/mentor_rejection_checklist.md`
