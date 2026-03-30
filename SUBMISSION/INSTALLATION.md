# Installation Guide

This guide covers local setup for development, evaluation, and verification.

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Git

## Repository Setup

```bash
git clone https://github.com/fallofpheonix/AI4MH.git
cd AI4MH
```

## Backend Setup

```bash
cd backend
python3 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Sanity check:

```bash
./.venv312/bin/python - <<'PY'
from app.main import create_app
from app.core.config import settings

app = create_app()
print(app.title)
print(settings.api_prefix)
print(settings.sqlite_path)
PY
```

## Frontend Setup

```bash
cd frontend
npm install
npm run build
```

## Running Locally

Backend:

```bash
cd backend
source .venv312/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## Runtime URLs

- Backend docs: `http://127.0.0.1:8000/docs`
- Versioned API: `http://127.0.0.1:8000/api/v1`
- Frontend dashboard: `http://127.0.0.1:5173`

## Configuration

Primary settings live in `backend/app/core/config.py`.

Common environment variables:

```bash
AI4MH_API_PREFIX=/api
AI4MH_ALERT_THRESHOLD=0.75
AI4MH_MAX_POSTS=500
AI4MH_DEFAULT_INGEST_BATCH_SIZE=30
AI4MH_BOOTSTRAP_BATCH_SIZE=120
AI4MH_SQLITE_PATH=ai4mh.db
AI4MH_ALLOWED_ORIGINS='["http://localhost:3000","http://localhost:4173","http://localhost:5173","http://127.0.0.1:3000","http://127.0.0.1:4173","http://127.0.0.1:5173"]'
```

Advanced overrides use JSON strings:

```bash
AI4MH_WEIGHTS='{"sentiment":0.35,"volume":0.30,"geo_cluster":0.20,"trend":0.15}'
AI4MH_ESCALATION_THRESHOLDS='{"crisis_score":0.70,"confidence":0.60,"min_posts":10,"max_bot_ratio":0.25}'
```

## Troubleshooting

### FastAPI import errors

```bash
cd backend
source .venv312/bin/activate
python -m pip install -r requirements.txt
```

### Frontend cannot reach backend

- Verify backend is listening on `127.0.0.1:8000`
- Verify the frontend uses `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1` or `http://localhost:8000/api/v1`
- Check `AI4MH_ALLOWED_ORIGINS` if you changed host or port

### Reset local SQLite state

```bash
cd backend
rm -f ai4mh.db ai4mh.db-shm ai4mh.db-wal
```

## Post-Install Validation

```bash
cd backend
./.venv312/bin/python -m pytest

cd ../frontend
npm run build

cd ..
bash scripts/full_health_check.sh
```
