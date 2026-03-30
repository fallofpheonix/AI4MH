# Contributing to AI4MH

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git

## Local Setup

```bash
git clone https://github.com/fallofpheonix/AI4MH.git
cd AI4MH

cd backend
python3 -m venv .venv312
source .venv312/bin/activate
python -m pip install -r requirements.txt

cd ../frontend
npm install
```

## Run Locally

Backend:

```bash
cd backend
source .venv312/bin/activate
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

Runtime URLs:

- API docs: `http://127.0.0.1:8000/docs`
- API base: `http://127.0.0.1:8000/api/v1`
- Dashboard: `http://127.0.0.1:5173`

## Validation Before PR

```bash
cd backend
./.venv312/bin/python -m pytest

cd ../frontend
npm run build

cd ..
bash scripts/full_health_check.sh
```

## Repository Conventions

### Backend

- Keep API handlers thin.
- Put orchestration and business logic in `backend/app/services`.
- Put persistence contracts and implementations in `backend/app/crud`.
- Put typed payload models in `backend/app/schemas`.
- Put runtime settings and application wiring in `backend/app/core`.

### Frontend

- Keep page composition in `frontend/src/pages`.
- Keep stateful orchestration in `frontend/src/hooks`.
- Keep network code in `frontend/src/services`.
- Keep reusable UI in `frontend/src/components/common` and `frontend/src/components/layout`.
- Keep domain-specific UI in `frontend/src/components/features`.
- Use `@` imports for `frontend/src/*`.

## Documentation Rules

Update documentation when changing:

- API routes or payloads
- environment variables
- repository layout
- verification or deployment steps

Minimum files to consider:

- `README.md`
- `docs/ARCHITECTURE.md`
- `SUBMISSION/*.md`
- `SUBMISSION/docs/*.md`

## Commit Guidelines

- Keep commits scoped to one concern.
- Use descriptive messages.
- Do not mix structural refactors with unrelated logic changes unless necessary to keep the tree buildable.
