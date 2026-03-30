# DECISIONS

| Decision | Reason | Consequence |
|---|---|---|
| synthetic ingestion instead of live APIs | deterministic demo, no secrets, no external dependency risk | not representative of production traffic |
| white-box weighted scoring instead of opaque ML | explainability and governance | lower modeling sophistication |
| versioned HTTP surface under `/api/v1` | preserve forward-compatibility | clients must target versioned path |
| `crud.Store` abstraction instead of direct route-level DB usage | isolate persistence concerns | more files, but swappable storage |
| SQLite JSON blob persistence | low setup cost and portable local runtime | limited query flexibility and no migrations |
| in-memory store for tests | fast deterministic test setup | not representative of production persistence behavior |
| polling frontend instead of realtime push | simpler client/server model | extra request load and stale-window latency |
| modular frontend with `@` alias | reduce import churn and improve structure | requires Vite/jsconfig alias maintenance |
