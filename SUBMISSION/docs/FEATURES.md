# Feature Checklist

This checklist reflects the current repository, not aspirational or removed modules.

## Backend

- [x] Synthetic post generation
- [x] VADER sentiment enrichment
- [x] Crisis keyword matching
- [x] Region-level scoring
- [x] Confidence calculation with bot-ratio impact
- [x] Alert generation and lifecycle persistence
- [x] Bias diagnostics by population tier
- [x] SQLite-backed persistence with WAL mode
- [x] In-memory store for tests
- [x] Versioned FastAPI routes under `/api/v1`

## Frontend

- [x] React/Vite dashboard
- [x] Modular page/layout/component structure
- [x] Shared API client and dashboard service layer
- [x] Polling-based refresh loop
- [x] Manual ingest trigger
- [x] Alert list
- [x] Recent posts table
- [x] Log viewer
- [x] Build-time aliasing with `@`

## Documentation and Operations

- [x] Root README updated to current layout
- [x] Architecture doc updated to current layout
- [x] Submission docs aligned with `/api/v1`
- [x] Health-check script validates current endpoints
- [x] `.env.example` matches current settings surface

## Automated Validation

- [x] Backend pytest suite
- [x] Frontend production build
- [x] Full-stack shell health check

## Known Non-Features

- [ ] Real social API ingestion
- [ ] Authentication or authorization
- [ ] Dashboard controls for alert ack/dismiss/resolve
- [ ] Docker deployment assets in-repo
- [ ] Frontend unit/integration test runner
