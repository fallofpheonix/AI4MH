# AI4MH — AI for Mental Health

AI4MH is a full-stack demo system for regional mental-health crisis signal monitoring. It ingests synthetic social discussion posts, enriches them with VADER sentiment analysis and crisis keyword matching, aggregates per-region crisis scores using a weighted formula, and persists alert state in SQLite. The results are exposed through a FastAPI REST API and a React/Vite dashboard.

The project exists to illustrate how a responsible, decision-support pipeline for mental-health signal monitoring could be structured — not to replace clinical judgement or human intervention.

Supported local Python versions: `3.10` to `3.12`

## Purpose and Ethical Scope

This project is a **demonstration tool only**:

- **Synthetic ingestion only.** There are no live social-media connectors or real user data.
- **Alerts are decision-support outputs, not automated interventions.** Every alert requires a human operator to review and act.
- **Storage is local SQLite** for demo reproducibility. There is no production database, authentication, or multi-user access control.
- **Bias guardrails are informational.** The `/bias` endpoint surfaces per-tier fairness metrics; these are guardrails, not proof of fairness.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.10–3.12, FastAPI 0.111, Uvicorn |
| Sentiment analysis | VADER (`vaderSentiment`) |
| Data validation | Pydantic v2 |
| Persistence | SQLite (WAL mode) via `sqlite3` |
| Frontend | React 18, Vite, JavaScript |
| Containerisation | Docker / Docker Compose |
| Testing | pytest, httpx |

## Repository Layout

```text
backend/   FastAPI service, scoring pipeline, SQLite persistence, tests
frontend/  React/Vite dashboard
data/      Minimal runtime sample data (lexicons)
docs/      Architecture, API reference, and demo notes
scripts/   Development smoke-check helper
```

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Backend default address: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Frontend default address: `http://127.0.0.1:5173`

### Full Stack Smoke Check

From the repo root:

```bash
bash scripts/full_health_check.sh
```

This script bootstraps local backend/frontend dependencies, starts both services, and validates the HTTP surface.

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and adjust as needed.

| Variable | Default | Description |
|---|---|---|
| `AI4MH_API_PREFIX` | `/api` | URL prefix for the API router |
| `AI4MH_MAX_POSTS` | `500` | Maximum posts retained in SQLite |
| `AI4MH_DEFAULT_INGEST_BATCH_SIZE` | `30` | Posts generated per manual ingest cycle |
| `AI4MH_BOOTSTRAP_BATCH_SIZE` | `120` | Posts generated on first startup |
| `AI4MH_SQLITE_PATH` | `ai4mh.db` | SQLite database file path |
| `AI4MH_ALLOWED_ORIGINS` | localhost variants | CORS allowed origins (JSON list) |

## Common Commands

```bash
make backend-install   # Create venv and install backend deps
make frontend-install  # npm ci for the frontend
make dev-backend       # Start backend with hot-reload
make dev-frontend      # Start Vite dev server
make test              # Run backend pytest suite
make build             # Run frontend production build
make smoke             # Full stack smoke check
```

## Docker Compose

```bash
docker compose up --build
```

This starts:

- backend on `http://localhost:8000`
- frontend on `http://localhost:80`

## API Surface

Base URL: `http://127.0.0.1:8000/api/v1`

| Method | Path | Description |
|---|---|---|
| `POST` | `/ingest?n=30` | Generate and process a synthetic batch |
| `GET` | `/posts?limit=60` | Return recent enriched posts |
| `GET` | `/scores` | Return current regional crisis scores |
| `GET` | `/alerts` | Return current alerts |
| `POST` | `/alerts/{id}/ack` | Transition alert to `acknowledged` |
| `POST` | `/alerts/{id}/dismiss` | Transition alert to `dismissed` |
| `POST` | `/alerts/{id}/resolve` | Transition alert to `resolved` |
| `GET` | `/logs?limit=100` | Return recent pipeline log events |
| `GET` | `/bias` | Return population-tier fairness metrics |

Full endpoint documentation: [docs/api.md](docs/api.md)

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Demo Notes](docs/demo.md)

## Validation

Backend tests:

```bash
make test
```

Frontend production build:

```bash
make build
```

## Contributing

1. Fork the repository and create a feature branch.
2. Install backend and frontend dependencies (`make install`).
3. Make your changes and ensure `make test` and `make build` pass.
4. Open a pull request with a clear description of the change.

## License

See [LICENSE](LICENSE).
