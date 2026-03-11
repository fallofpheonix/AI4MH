# AI4MH Project Documentation (Strict MVP)

## 1. Overview

AI4MH is a minimal crisis-signal monitoring prototype for the GSoC contributor task.

The system ingests social-style posts, enriches them with NLP sentiment/crisis flags, computes regional crisis scores, produces review-required alerts, and exposes all outputs through a simple API consumed by a single-page React frontend.

## 2. Scope

Included:

- Synthetic post ingestion
- NLP enrichment (VADER + crisis terms)
- Regional scoring
- Threshold-based alerts
- Basic event logging
- Frontend monitoring dashboard

Excluded by design:

- Production database
- Authentication/authorization
- Real social platform ingestion
- Advanced ML model training

## 3. Runtime Architecture

```text
Ingest Posts -> NLP Enrichment -> Region Scoring -> Alert Thresholding -> Logs
      \                                                      |
       +------------------- API (FastAPI) -------------------+
                                   |
                           React Dashboard
```

## 4. Repository Layout

```text
backend/
  main.py                 # API + orchestration
  ingest_posts.py         # synthetic data generation
  nlp_processing.py       # sentiment + keyword analysis
  crisis_scoring.py       # region-level crisis scoring
  requirements.txt

frontend/
  src/App.jsx             # one-page monitor
  src/main.jsx            # app bootstrap
  package.json

scripts/
  full_health_check.sh    # start/check/validate stack

ANSWER.md                 # evaluator-facing direct answer
README.md                 # quickstart and doc index
```

## 5. Backend Details

### 5.1 Data Flow (`backend/main.py`)

1. `POST /api/ingest?n=30` triggers `_refresh(n)`.
2. `_refresh` does:
   - `generate_dataset(n)`
   - `analyze_batch(posts)`
   - `score_all_regions(all_posts)`
3. Alerts are generated when `crisis_score > 0.75`.
4. Events are appended to in-memory `_logs`.

### 5.2 In-Memory State

- `_posts`: latest enriched posts (max 500)
- `_scores`: latest regional score snapshots
- `_alerts`: current threshold alerts
- `_logs`: append-only event records

### 5.3 API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/posts?limit=60` | Latest enriched posts |
| GET | `/api/scores` | Regional scores |
| GET | `/api/alerts` | Current review-required alerts |
| GET | `/api/logs?limit=100` | Recent event logs |
| POST | `/api/ingest?n=30` | Trigger ingest + score refresh |

## 6. Scoring Logic

Implemented in `backend/crisis_scoring.py`.

Signals:

- `sentiment_intensity`
- `volume_spike`
- `geo_cluster`
- `trend_accel`

Composite score:

```text
crisis_score =
  0.35 * sentiment_intensity +
  0.30 * volume_spike +
  0.20 * geo_cluster +
  0.15 * trend_accel
```

Confidence is estimated from sample volume/consistency/coverage in the current MVP logic.

## 7. Frontend Details

Implemented in `frontend/src/App.jsx`.

Single-page UI includes:

- Ingest button
- Pause/Resume live mode
- Alerts panel
- Recent posts table
- Basic event log view

Live mode behavior:

- When enabled, frontend triggers ingest every 5 seconds.

## 8. Setup and Run

### 8.1 Backend

```bash
cd backend
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 8.2 Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Access:

- Frontend: `http://127.0.0.1:5173`
- Backend scores: `http://127.0.0.1:8000/api/scores`

## 9. Verification

One-command stack check:

```bash
./scripts/full_health_check.sh
```

Validation-only (if already running):

```bash
./scripts/full_health_check.sh --no-start
```

## 10. Troubleshooting

### Backend not reachable

- Confirm backend is running on `:8000`.
- Check `backend/.venv312` activation.

### Frontend loads but no data

- Verify CORS hosts in `backend/main.py` include `http://localhost:5173`.
- Check browser dev tools for failed API calls.

### Repeated ingest calls

- Live mode is enabled by default.
- Click `Pause` to stop automatic ingest.

## 11. Submission Alignment

This MVP directly supports the task deliverables:

1. Crisis Signal Design: scoring pipeline and thresholds
2. Governance/Risk Controls: alert gating + logs + human-review-required status
3. Governance Reflection: documented in `ANSWER.md`

For evaluator-first content, read `ANSWER.md`.
