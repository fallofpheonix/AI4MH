#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_URL="${API_URL:-http://127.0.0.1:8000}"
WEB_URL="${WEB_URL:-http://127.0.0.1:5173}"
START_SERVICES=1

if [[ "${1:-}" == "--no-start" ]]; then
  START_SERVICES=0
fi

BACK_PID=""
FRONT_PID=""

cleanup() {
  if [[ -n "$BACK_PID" ]]; then
    kill "$BACK_PID" >/dev/null 2>&1 || true
  fi
  if [[ -n "$FRONT_PID" ]]; then
    kill "$FRONT_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

wait_for_url() {
  local url="$1"
  local retries="${2:-120}"
  local delay="${3:-0.5}"
  local i
  for ((i=1; i<=retries; i++)); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep "$delay"
  done
  echo "timeout waiting for $url" >&2
  return 1
}

assert_json() {
  local payload="$1"
  local python_expr="$2"
  JSON_PAYLOAD="$payload" PY_EXPR="$python_expr" python3 - <<'PY'
import json
import os

payload = os.environ["JSON_PAYLOAD"]
expr = os.environ["PY_EXPR"]
data = json.loads(payload)
if not eval(expr, {}, {"data": data}):
    raise SystemExit(f"json assertion failed: {expr}")
PY
}

if [[ "$START_SERVICES" -eq 1 ]]; then
  # Ensure no stale processes are holding ports.
  lsof -ti tcp:8000 | xargs kill -9 >/dev/null 2>&1 || true
  lsof -ti tcp:5173 | xargs kill -9 >/dev/null 2>&1 || true

  echo "[1/5] Starting backend"
  cd "$ROOT_DIR/backend"
  if [[ ! -d .venv312 ]]; then
    python3.12 -m venv .venv312
  fi
  # shellcheck disable=SC1091
  source .venv312/bin/activate
  if ! python -c "import fastapi,uvicorn,vaderSentiment,pydantic" >/dev/null 2>&1; then
    pip install -q -r requirements.txt
  fi
  nohup uvicorn main:app --host 127.0.0.1 --port 8000 > /tmp/ai4mh_health_backend.log 2>&1 &
  BACK_PID=$!

  echo "[2/5] Starting frontend"
  cd "$ROOT_DIR/frontend"
  if [[ ! -d node_modules ]]; then
    npm install --silent
  fi
  nohup npm run dev -- --host 127.0.0.1 --port 5173 > /tmp/ai4mh_health_frontend.log 2>&1 &
  FRONT_PID=$!
fi

echo "[3/5] Waiting for services"
wait_for_url "$API_URL/api/scores"
wait_for_url "$WEB_URL"

echo "[4/5] Validating API"
POSTS="$(curl -fsS "$API_URL/api/posts?limit=3")"
assert_json "$POSTS" "isinstance(data.get('posts'), list) and len(data.get('posts')) == 3"
SCORES="$(curl -fsS "$API_URL/api/scores")"
assert_json "$SCORES" "isinstance(data.get('scores'), list)"

ALERTS="$(curl -fsS "$API_URL/api/alerts")"
assert_json "$ALERTS" "isinstance(data.get('alerts'), list)"

LOGS="$(curl -fsS "$API_URL/api/logs?limit=20")"
assert_json "$LOGS" "isinstance(data.get('logs'), list)"

INGEST="$(curl -fsS -X POST "$API_URL/api/ingest?n=5")"
assert_json "$INGEST" "'total_posts' in data and 'regions_scored' in data and 'alerts' in data"

echo "[5/5] Validating frontend"
FRONT_HTML="$(curl -fsS "$WEB_URL")"
if [[ "$FRONT_HTML" != *"<div id=\"root\"></div>"* ]]; then
  echo "frontend check failed: root element missing" >&2
  exit 1
fi

echo "PASS: full health check completed"
