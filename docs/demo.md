# Demo Notes

## System Behaviour on Startup

When the backend starts for the first time (empty database) it automatically runs one bootstrap pipeline cycle of 120 synthetic posts. This seeds all four SQLite tables so the dashboard has something to display immediately without needing a manual ingest.

Subsequent restarts reuse the existing database. Pass a fresh `AI4MH_SQLITE_PATH` to start clean.

## What the Dashboard Shows

| Section | Content |
|---|---|
| **Metric pills** (top bar) | Live counts of visible posts, scored regions, and active alerts |
| **Alerts** | All alerts with status, region, score, and action buttons (Ack / Dismiss / Resolve) |
| **Posts table** | Most recent enriched posts with sentiment, NLP flag, and region crisis score |
| **Logs** | Last 20 pipeline events ordered by time ascending |

## Manual Demo Flow

1. Start the backend (`make dev-backend` or `docker compose up --build`).
2. Start the frontend (`make dev-frontend`).
3. Open the dashboard at `http://localhost:5173` (or `http://localhost:80` with Docker).
4. Click **Ingest Posts** to trigger a manual cycle of 30 synthetic posts.
5. Observe:
   - **Posts** count increases.
   - **Regions** count reflects all scored regions.
   - **Logs** appends an `ingest_completed` event.
   - **Alerts** panel populates when any region crosses the escalation threshold (`crisis_score ≥ 0.70`, `confidence ≥ 0.60`, `post_count ≥ 10`, `bot_ratio < 0.25`).
6. Click **Ack**, **Dismiss**, or **Resolve** on an alert to change its status. The action is reflected immediately.

## Live Mode

The dashboard has a **Pause / Resume** toggle next to the Ingest button.

- **Resume** (default on load) — triggers a full ingest cycle every 5 seconds automatically.
- **Pause** — stops the timer; the dashboard retains its last state.

Live mode exists for demonstration purposes only. It is not production-safe ingestion orchestration.

## Scoring Escalation

A region raises an alert only when all four conditions are met simultaneously:

```
crisis_score  ≥ 0.70   (weighted blend of sentiment, volume, cluster, trend)
confidence    ≥ 0.60
post_count    ≥ 10     (clean / non-bot posts only)
bot_ratio     < 0.25
```

Because the synthetic data is random, not every ingest cycle will produce alerts. Running several cycles (or using a larger `n`) increases the probability of seeing alerts.

## Verification Commands

Backend tests:

```bash
cd backend
pytest tests
```

Frontend production build:

```bash
cd frontend
npm run build
```

Full stack smoke check (starts both servers locally and validates the HTTP surface):

```bash
bash scripts/full_health_check.sh
```

## Known Limits

- Ingestion is random and non-deterministic between runs.
- There is no authentication, operator identity, or session model.
- SQLite is a local demo store — not suitable for concurrent production use.
- Alerts are local workflow state only; there is no external incident integration.
- The frontend has no automated test suite.
