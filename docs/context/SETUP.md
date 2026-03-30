# SETUP

## Requirements

- Python `3.10+`
- Node.js `18+`
- npm

## Backend

```bash
cd backend
python3 -m venv .venv312
source .venv312/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Run:

```bash
cd backend
source .venv312/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## Build / Test

```bash
cd backend
./.venv312/bin/python -m pytest

cd ../frontend
npm run build

cd ..
bash scripts/full_health_check.sh
```

## Environment Variables

- `AI4MH_API_PREFIX`
- `AI4MH_ALERT_THRESHOLD`
- `AI4MH_MAX_POSTS`
- `AI4MH_DEFAULT_INGEST_BATCH_SIZE`
- `AI4MH_BOOTSTRAP_BATCH_SIZE`
- `AI4MH_SQLITE_PATH`
- `AI4MH_ALLOWED_ORIGINS`
- `AI4MH_WEIGHTS`
- `AI4MH_ESCALATION_THRESHOLDS`
- `VITE_API_BASE_URL`

## Default Runtime URLs

- backend docs: `http://127.0.0.1:8000/docs`
- API base: `http://127.0.0.1:8000/api/v1`
- frontend: `http://127.0.0.1:5173`
