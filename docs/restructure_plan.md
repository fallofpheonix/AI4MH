# Restructure Plan

## Inputs

- Project root: `/Users/fallofpheonix/Project/Human AI/done/AI4MH`
- Tech stack: Python + FastAPI backend, React + Vite frontend, SQLite persistence
- Project type: web application

## 1. Current Structure Assessment

### Active Source Layout

```text
backend/
  app/
    api/
    core/
    crud/
    schemas/
    services/
    utils/
  tests/

frontend/
  src/
    components/
    hooks/
    pages/
    services/
    styles/
    utils/

docs/
SUBMISSION/
scripts/
```

### Findings

#### Good

- Backend is already modularized by responsibility.
- Frontend is already modularized by page, service, hook, and component role.
- API versioning exists.
- Tests are separated from app code.

#### Cleanup Required

- Root contains redundant documentation sets:
  - `README.md`
  - `docs/*`
  - `SUBMISSION/*`
  - `SUBMISSION_CHECKLIST.md`
  - `docs/context/*`
- Backend runtime artifacts live inside the repo tree:
  - `backend/ai4mh.db*`
  - `backend/.pytest_cache/`
  - `backend/__pycache__/`
  - local venvs
- Legacy deleted-package bytecode still exists:
  - `backend/app/api/routes/__pycache__/...`
  - `backend/app/config/__pycache__/...`
  - `backend/app/core/models/__pycache__/...`
  - `backend/app/core/stores/__pycache__/...`
  - `backend/__pycache__/crisis_scoring.cpython-312.pyc`
  - `backend/__pycache__/ingest_posts.cpython-312.pyc`
  - `backend/__pycache__/nlp_processing.cpython-312.pyc`
- Naming is mixed:
  - docs use uppercase names
  - source tree uses lowercase / package-style naming
- `backend/app/crud/` is semantically a storage layer, not CRUD services.
- `backend/main.py` is a compatibility wrapper duplicating the real ASGI entrypoint.
- `SUBMISSION/deployment/` is empty.
- `frontend/src/assets/.gitkeep` is empty and unused.

#### Dead / Duplicate Logic

- No major duplicate business logic remains in active source modules.
- The only clear tracked source duplication is the entrypoint wrapper `backend/main.py`.
- The biggest redundancy is documentation duplication, not runtime logic duplication.

## 2. Target Structure

```text
root/
  backend/
    app/
      api/
        dependencies.py
        v1/
          router.py
          routes/
      core/
        config.py
        container.py
      storage/
        base.py
        memory.py
        sqlite.py
      schemas/
      services/
      utils/
      main.py
    tests/
    .env.example
    pyproject.toml
    requirements.txt
  frontend/
    src/
      components/
        common/
        features/
        layout/
      hooks/
      pages/
      services/
      styles/
      utils/
      App.jsx
      main.jsx
    index.html
    jsconfig.json
    package.json
    vite.config.js
  docs/
    architecture.md
    spec.md
    roadmap.md
    submission/
      readme.md
      installation.md
      testing.md
      verification.md
      deployment.md
      api_reference.md
      features.md
      governance.md
      checklist.md
    context/
  scripts/
  var/              # ignored runtime DB/logs/pids
  .gitignore
  README.md
  CONTRIBUTING.md
  LICENSE
```

### Structural Decisions

- Keep backend and frontend as separate deployable/workable units.
- Rename `crud` to `storage` because the package contains persistence adapters, not CRUD business operations.
- Keep `schemas` until API/domain models diverge enough to justify `domain/` + `dto/`.
- Consolidate all non-user-facing long-form docs under `docs/`.
- Move runtime-generated state out of `backend/` into ignored `var/`.
- Remove the wrapper entrypoint and use `app.main:app` as the single backend entrypoint.

## 3. File Reassignment Plan

Unlisted tracked files stay in place.

| Old Path | Action |
|---|---|
| `backend/app/crud/__init__.py` | `backend/app/storage/__init__.py` |
| `backend/app/crud/base.py` | `backend/app/storage/base.py` |
| `backend/app/crud/memory.py` | `backend/app/storage/memory.py` |
| `backend/app/crud/sqlite.py` | `backend/app/storage/sqlite.py` |
| `backend/main.py` | `DELETE` after all launch commands use `app.main:app` |
| `docs/ARCHITECTURE.md` | `docs/architecture.md` |
| `docs/PROJECT_SPEC.md` | `docs/spec.md` |
| `docs/ROADMAP.md` | `docs/roadmap.md` |
| `docs/gsoc_proposal.md` | `docs/archive/gsoc_proposal.md` |
| `SUBMISSION/README.md` | `docs/submission/readme.md` |
| `SUBMISSION/INSTALLATION.md` | `docs/submission/installation.md` |
| `SUBMISSION/TESTING.md` | `docs/submission/testing.md` |
| `SUBMISSION/VERIFICATION.md` | `docs/submission/verification.md` |
| `SUBMISSION/DEPLOYMENT.md` | `docs/submission/deployment.md` |
| `SUBMISSION/docs/API_REFERENCE.md` | `docs/submission/api_reference.md` |
| `SUBMISSION/docs/FEATURES.md` | `docs/submission/features.md` |
| `SUBMISSION/docs/GOVERNANCE.md` | `docs/submission/governance.md` |
| `SUBMISSION_CHECKLIST.md` | `docs/submission/checklist.md` |
| `SUBMISSION/deployment/` | `DELETE` |
| `frontend/src/assets/.gitkeep` | `DELETE` |
| `backend/ai4mh.db*` | move runtime output to `var/ai4mh.db*` and ignore |
| `.venv/` | `DELETE` local artifact |
| `backend/.venv312/` | keep local only, not part of repo plan |
| `backend/.venv_ai4mh/` | `DELETE` or standardize to one venv |
| `backend/.pytest_cache/` | `DELETE` local artifact |
| `backend/__pycache__/` | `DELETE` local artifact |
| `backend/app/api/routes/__pycache__/` | `DELETE` stale bytecode |
| `backend/app/config/__pycache__/` | `DELETE` stale bytecode |
| `backend/app/core/models/__pycache__/` | `DELETE` stale bytecode |
| `backend/app/core/stores/__pycache__/` | `DELETE` stale bytecode |

## 4. Code Cleanup Plan

### Remove

- wrapper backend entrypoint: `backend/main.py`
- empty asset placeholder: `frontend/src/assets/.gitkeep`
- stale runtime artifacts and bytecode directories

### Refactor

- rename `app.crud` imports to `app.storage`
- centralize all backend launch commands on `uvicorn app.main:app`
- centralize docs under `docs/`
- change SQLite default path from `backend/ai4mh.db` to ignored `var/ai4mh.db`

### Keep

- `frontend/src/App.jsx` as UI root wrapper
- `frontend/src/components/common/*` despite small size; they preserve UI composition boundaries
- `backend/app/schemas/*` until request/response and domain models diverge

## 5. Standardization

### Naming

- Python packages/files: `snake_case`
- React components: `PascalCase`
- hooks: `useXxx`
- docs: lowercase filenames under `docs/`

### Config

- backend runtime config stays in `backend/app/core/config.py`
- frontend build config stays in `frontend/vite.config.js`
- keep `.env.example`
- add ignored `var/` to `.gitignore`

## 6. Dependency + Entry Point Fixes

- Replace all `app.crud` imports with `app.storage`
- Replace `uvicorn main:app` with `uvicorn app.main:app`
- Replace `gunicorn main:app` with `gunicorn app.main:app`
- Update health check, README, CONTRIBUTING, submission docs, and deployment docs accordingly

## 7. Ordered Migration Steps

1. Create `backend/app/storage/`.
2. Move files from `backend/app/crud/` to `backend/app/storage/`.
3. Rewrite Python imports from `app.crud` to `app.storage`.
4. Update backend docs/scripts/service examples to `app.main:app`.
5. Delete `backend/main.py`.
6. Move `SUBMISSION/*` into `docs/submission/`.
7. Rename docs to lowercase names.
8. Move `docs/gsoc_proposal.md` into `docs/archive/`.
9. Add ignored `var/` and point `AI4MH_SQLITE_PATH` there by default.
10. Delete `.gitkeep`, caches, bytecode, local DB files, extra venvs, and empty submission deployment dir.
11. Run:
    - `cd backend && ./.venv312/bin/python -m pytest`
    - `cd frontend && npm run build`
    - `bash scripts/full_health_check.sh`

## 8. Deletions

- `backend/main.py`
- `SUBMISSION/deployment/`
- `frontend/src/assets/.gitkeep`
- `.venv/`
- `backend/.venv_ai4mh/`
- `backend/.pytest_cache/`
- `backend/__pycache__/`
- `backend/app/api/routes/__pycache__/`
- `backend/app/config/__pycache__/`
- `backend/app/core/models/__pycache__/`
- `backend/app/core/stores/__pycache__/`
- `backend/ai4mh.db`
- `backend/ai4mh.db-shm`
- `backend/ai4mh.db-wal`

## 9. Risks / Breaking Changes

- Renaming `crud` to `storage` breaks imports across backend code and tests until all references are updated.
- Removing `backend/main.py` breaks any script or deployment config still using `main:app`.
- Moving docs breaks direct links unless README and external references are updated.
- Changing SQLite default path changes local operational behavior and any scripts assuming DB under `backend/`.
