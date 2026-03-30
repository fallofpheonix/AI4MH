# Testing Guide

This repository currently validates backend behavior with pytest, frontend packaging with a production build, and full-stack behavior with a shell health check.

## Test Inventory

Backend tests:

- `backend/tests/test_scoring.py`
  - `test_score_region_skips_all_bot_traffic`
  - `test_score_region_escalates_for_strong_signal`
  - `test_score_regions_keeps_results_sorted`
- `backend/tests/test_api.py`
  - `test_ingest_returns_operational_summary`
  - `test_monitoring_endpoints_return_expected_shapes`
  - `test_alert_lifecycle_writes_log_entry`
  - `test_unknown_alert_returns_404`

Current total: `7` backend tests.

## Run Backend Tests

```bash
cd backend
./.venv312/bin/python -m pytest
```

Run a subset:

```bash
cd backend
./.venv312/bin/python -m pytest tests/test_scoring.py -q
./.venv312/bin/python -m pytest tests/test_api.py -q
```

## Run Frontend Build Validation

```bash
cd frontend
npm run build
```

This catches broken imports, alias issues, and invalid JSX.

## Run Full-Stack Health Check

```bash
bash scripts/full_health_check.sh
```

The script:

- starts backend and frontend if needed
- waits for both services
- validates `/api/v1` endpoints
- validates the frontend root page

If services are already running:

```bash
bash scripts/full_health_check.sh --no-start
```

## Expected Results

- `pytest`: `7 passed`
- frontend build: Vite build succeeds
- health check: `PASS: full health check completed`

## Known Non-Failing Warning

Pytest may emit the Starlette `python_multipart` pending deprecation warning. That warning is upstream and does not fail the suite.

## Gaps

- No frontend unit/integration test framework is configured
- No performance/load test suite is checked into the repo
- No CI workflow is present in the repository at this time
