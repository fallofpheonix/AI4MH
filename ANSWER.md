# AI4MH - Direct Answer (Strict MVP)

## Problem
Determine whether rising crisis-related social signals across Alabama counties are credible enough to escalate to human review.

## Scenario
Within 72 hours, three counties show increased negative sentiment and suicide-related language. The system decides whether escalation is warranted.

## Deliverable 1: Crisis Signal Design (Core Component)
Implemented in:
- `backend/nlp_processing.py`
- `backend/crisis_scoring.py`
- `backend/main.py`

Implemented logic:
- Sentiment intensity
- Volume spike detection
- Geographic clustering
- Minimum sample-size gate
- Simple stabilization and confidence handling in scoring pipeline

Core scoring form:
```text
crisis_score = 0.35*sentiment + 0.30*volume_spike + 0.20*geo_cluster + 0.15*trend_accel
```

## Deliverable 2: Governance & Risk Controls
Implemented in strict MVP form in `backend/main.py`:
- Alert threshold (`score > 0.75`)
- Human review required for alerted regions
- Structured event logging (`/api/logs`)

## Deliverable 3: Governance Reflection (Short)
- Primary risk: false crisis escalation from noisy/manipulated social signals.
- Most important safeguard: human verification before operational escalation.

## Evaluation Criteria Mapping

1. Systems thinking: complete runnable pipeline (ingest -> NLP -> score -> alert -> logs -> UI).
2. Responsible AI/governance: threshold-based escalation + human review requirement + logs.
3. Bias/mitigation awareness: regional aggregation + confidence and sample-size safeguards.
4. Uncertainty treatment: confidence available in region scores.
5. Communication: direct deliverable-to-code mapping.

## Working API (Strict MVP)
- `POST /api/ingest?n=30`
- `GET /api/posts?limit=60`
- `GET /api/scores`
- `GET /api/alerts`
- `GET /api/logs?limit=100`

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
