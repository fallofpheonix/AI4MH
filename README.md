# AI4MH

AI4MH is a governance-first crisis monitoring prototype for early detection of suicide, substance-use, and mental-health distress signals from online discussion streams. The repository is intentionally small: one backend, one frontend, and a small set of canonical markdown documents that define scope, architecture, and development direction.

## Primary Project Documents

These files are the authoritative source for future development:

- [docs/PROJECT_SPEC.md](/Users/fallofpheonix/Project/Human AI/AI4MH/docs/PROJECT_SPEC.md)
- [docs/ARCHITECTURE.md](/Users/fallofpheonix/Project/Human AI/AI4MH/docs/ARCHITECTURE.md)
- [docs/ROADMAP.md](/Users/fallofpheonix/Project/Human AI/AI4MH/docs/ROADMAP.md)

## Repository Scope

- `backend/`: FastAPI service, ingestion, NLP enrichment, regional scoring.
- `frontend/`: single-page monitoring UI.
- `scripts/full_health_check.sh`: end-to-end local validation.
- `index.md`: GitHub Pages project page.

## Runtime Pipeline

```text
Posts -> NLP Enrichment -> Regional Aggregation -> Crisis Score
      -> Confidence -> Escalation Gate -> Alerts + Logs -> UI
```

## Core Rules

- No automated intervention.
- Escalation means `review_required` only.
- Regional outputs must include `crisis_score` and `confidence`.
- Logs remain append-only for traceability.

## Local Run

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

## Validation

```bash
./scripts/full_health_check.sh
```

## License

No license file is currently defined in the repository.
