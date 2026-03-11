# AI4MH (AI for Mental Health Crisis Monitoring)

Read this first: `ANSWER.md`.

## Submission Scope
This repository provides a direct implementation response for the AI4MH contributor-selection task:

1. Crisis Signal Design
2. Governance & Risk Controls
3. Governance Reflection

All three are mapped to code and execution steps in `ANSWER.md`.

## Quick Run
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

## Quick Validation
```bash
./scripts/full_health_check.sh --no-start
```

## Key Files
- `ANSWER.md`
- `backend/main.py`
- `backend/nlp_processing.py`
- `backend/crisis_scoring.py`
- `frontend/src/App.jsx`
- `scripts/full_health_check.sh`
