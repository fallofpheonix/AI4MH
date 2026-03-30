# Verification Guide

Follow these steps to verify that the repository is runnable end-to-end.

## 1. Verify Backend Imports

```bash
cd backend
source .venv312/bin/activate
python - <<'PY'
from app.main import create_app
from app.core.config import settings

app = create_app()
assert app.title == settings.app_name
print("app:", app.title)
print("api_prefix:", settings.api_prefix)
print("sqlite_path:", settings.sqlite_path)
PY
```

## 2. Verify Backend Tests

```bash
cd backend
./.venv312/bin/python -m pytest
```

Expected result:

```text
7 passed
```

## 3. Verify Frontend Build

```bash
cd frontend
npm run build
```

## 4. Start Services

Backend:

```bash
cd backend
source .venv312/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## 5. Verify API Endpoints

```bash
curl -s http://127.0.0.1:8000/api/v1/posts?limit=5 | python3 -m json.tool | head -20
curl -s http://127.0.0.1:8000/api/v1/scores | python3 -m json.tool | head -20
curl -s http://127.0.0.1:8000/api/v1/alerts | python3 -m json.tool | head -20
curl -s http://127.0.0.1:8000/api/v1/logs?limit=5 | python3 -m json.tool | head -20
curl -s http://127.0.0.1:8000/api/v1/bias | python3 -m json.tool | head -20
curl -s -X POST "http://127.0.0.1:8000/api/v1/ingest?n=5" | python3 -m json.tool
```

Expected properties:

- `/posts`: `posts` list and `total`
- `/scores`: `scores` list and `updated_at`
- `/alerts`: `alerts` list
- `/logs`: `logs` list
- `/bias`: `by_tier`, `by_region`, `notes`, `as_of`
- `/ingest`: `total_posts`, `regions_scored`, `alerts`

## 6. Verify Frontend Behavior

Open `http://127.0.0.1:5173` and confirm:

- page title is `AI4MH Dashboard`
- header renders `AI4MH`
- buttons `Ingest Posts` and `Pause` are visible
- metrics for `Posts`, `Regions`, and `Alerts` are visible
- sections `Alerts`, `Recent Posts`, and `Logs` are visible
- clicking `Ingest Posts` refreshes data without console errors

## 7. Run Automated Full-Stack Check

If services are already running:

```bash
bash scripts/full_health_check.sh --no-start
```

If not:

```bash
bash scripts/full_health_check.sh
```

Expected terminal tail:

```text
[5/5] Validating frontend
PASS: full health check completed
```
