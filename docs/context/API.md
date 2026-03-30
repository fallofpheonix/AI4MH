# API

## HTTP Surface

Base URL:

```text
/api/v1
```

| Method | Path | Input | Output | Side Effect |
|---|---|---|---|---|
| `POST` | `/ingest?n=30` | query `n:int` | `total_posts`, `regions_scored`, `alerts` | generates posts, updates scores/alerts/logs |
| `GET` | `/posts?limit=60` | query `limit:int` | `posts[]`, `total` | none |
| `GET` | `/scores` | none | `scores[]`, `updated_at` | none |
| `GET` | `/alerts` | none | `alerts[]` | none |
| `POST` | `/alerts/{alert_id}/ack` | path `alert_id` | `alert` | updates alert, appends log |
| `POST` | `/alerts/{alert_id}/dismiss` | path `alert_id` | `alert` | updates alert, appends log |
| `POST` | `/alerts/{alert_id}/resolve` | path `alert_id` | `alert` | updates alert, appends log |
| `GET` | `/logs?limit=100` | query `limit:int` | `logs[]` | none |
| `GET` | `/bias` | none | `by_tier`, `by_region`, `notes`, `as_of` | none |

## Error Contract

- missing alert ID on transition: HTTP `404`
- frontend transport failure: hook sets UI error message

## Internal Interfaces

### `Store`

- `save_posts(posts)`
- `get_posts(limit=None)`
- `save_scores(scores)`
- `get_scores()`
- `save_alerts(alerts)`
- `get_alerts()`
- `get_alert(alert_id)`
- `update_alert(alert)`
- `append_log(event)`
- `get_logs(limit=100)`

### Frontend Service Layer

- `fetchDashboardSnapshot()`
  - fetches `/posts?limit=20`, `/scores`, `/alerts`, `/logs?limit=20`
  - returns `{ posts, scores, alerts, logs }`
- `ingestPosts(batchSize=30)`
  - posts to `/ingest?n=<batchSize>`

## Non-Contracts

- no auth headers
- no pagination beyond `limit`
- no request bodies for alert transitions
- no websocket or SSE interface
