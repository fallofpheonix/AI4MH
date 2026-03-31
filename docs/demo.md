# Demo Notes

## Expected Behavior

On backend startup, the pipeline bootstraps synthetic posts if the store is empty.

The frontend dashboard then shows:

- current alert list
- recent enriched posts
- recent log events
- region and post counts

## Manual Demo Flow

1. Start the backend.
2. Start the frontend.
3. Open the dashboard.
4. Trigger `Ingest Posts`.
5. Observe:
   - total posts increase
   - scores refresh
   - logs append `ingest_completed`
   - alerts appear when high-scoring regions are generated

## Polling Behavior

The frontend has a live mode toggle.

- `Resume` enables periodic ingestion every 5 seconds.
- `Pause` stops automated ingestion.

This is demo behavior, not production-safe ingestion orchestration.

## Verification Commands

Backend tests:

```bash
cd backend
pytest tests
```

Frontend build:

```bash
cd frontend
npm run build
```

Full smoke check:

```bash
bash scripts/full_health_check.sh
```

## Known Limits

- Ingestion is random and non-deterministic between runs.
- There is no authentication or operator identity model.
- SQLite is used as a local demo store.
- Alerts are local workflow state, not externally integrated incidents.
