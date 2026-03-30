# CONSTRAINTS

## Product Constraints

- highest automated alert state is `review_required`
- outputs must remain explainable
- sparse regions must not escalate easily
- bot-heavy traffic must reduce trust

## Technical Constraints

- storage is SQLite or in-memory only
- no ORM layer exists
- no auth/security subsystem exists
- API compatibility target is `/api/v1`
- frontend uses polling, not push transport

## Runtime Constraints

- `max_posts` defaults to `500`
- SQLite writes are serialized by a process-local lock
- `MemoryStore` and `SQLiteStore` are bounded by `max_posts`
- full ingest rescoring cost is dominated by stored post count

## Scoring Constraints

- score weights must sum to `1.0`
- escalation requires:
  - `crisis_score >= thresholds.crisis_score`
  - `confidence >= thresholds.confidence`
  - `post_count >= thresholds.min_posts`
  - `bot_ratio < thresholds.max_bot_ratio`

## Project Constraints

- current data is synthetic
- current dashboard is monitoring-first, not workflow-complete
- current repo has no container deployment assets
- no external deadline or milestone is encoded in the repo beyond roadmap priorities
