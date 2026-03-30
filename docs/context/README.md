# GPT Context Pack

Purpose: provide a low-entropy upload set for another GPT instance.

## Upload Order

1. `SPEC.md`
2. `ARCH.md`
3. `STATE.md`
4. `TASKS.md`
5. `API.md`
6. `DATA.md`
7. `SETUP.md`
8. `CONSTRAINTS.md`
9. `DECISIONS.md`
10. `EXPERIMENTS.md`
11. `ROADMAP.md`

## Minimum Viable Upload

If context budget is tight, upload:

- `SPEC.md`
- `ARCH.md`
- `STATE.md`
- `TASKS.md`
- key source files listed below

## Key Source Files To Upload After Docs

Backend:

- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/crud/base.py`
- `backend/app/services/pipeline_service.py`
- `backend/app/services/scoring_service.py`
- `backend/app/services/alert_service.py`
- `backend/app/services/enrichment_service.py`
- `backend/app/services/ingestion_service.py`
- `backend/app/schemas/post.py`
- `backend/app/schemas/score.py`
- `backend/app/schemas/alert.py`

Frontend:

- `frontend/src/pages/DashboardPage.jsx`
- `frontend/src/hooks/useDashboardData.js`
- `frontend/src/services/apiClient.js`
- `frontend/src/services/dashboardService.js`

Validation:

- `backend/tests/test_api.py`
- `backend/tests/test_scoring.py`
- `scripts/full_health_check.sh`
