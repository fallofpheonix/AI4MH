# API Reference

This document matches the current FastAPI implementation in `backend/app/api/v1/routes`.

## Base URL

```text
http://127.0.0.1:8000/api/v1
```

## Authentication

No authentication is implemented.

## Response Model

Responses are direct JSON payloads. There is no envelope such as `{"data": ..., "status": ...}`.

## Endpoints

### POST /ingest

Run one ingestion cycle.

Query parameters:

- `n` (`int`, optional, default `30`): number of synthetic posts to generate

Response:

```json
{
  "total_posts": 125,
  "regions_scored": 9,
  "alerts": 2
}
```

Example:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ingest?n=30"
```

### GET /posts

Return recent enriched posts.

Query parameters:

- `limit` (`int`, optional, default `60`)

Response shape:

```json
{
  "posts": [
    {
      "id": "post_123456",
      "text": "life feels completely hopeless",
      "subreddit": "depression",
      "region_id": "CA-LA",
      "region_name": "Los Angeles, CA",
      "timestamp": "2026-03-30T08:00:00+00:00",
      "upvotes": 120,
      "comments": 12,
      "is_bot": false,
      "is_crisis_text": true,
      "ground_truth_crisis": true,
      "sentiment": -0.5095,
      "keyword_count": 1,
      "keyword_terms": ["hopeless"],
      "nlp_crisis_flag": true,
      "ai_correct": true
    }
  ],
  "total": 125
}
```

Example:

```bash
curl "http://127.0.0.1:8000/api/v1/posts?limit=5"
```

### GET /scores

Return current region scores.

Response shape:

```json
{
  "scores": [
    {
      "region_id": "CA-LA",
      "post_count": 18,
      "bot_count": 1,
      "bot_ratio": 0.0526,
      "sentiment_intensity": 0.6111,
      "volume_spike": 0.4938,
      "geo_cluster": 0.5556,
      "trend_accel": 0.6667,
      "crisis_score": 0.5778,
      "confidence": 0.0616,
      "should_escalate": false,
      "avg_sentiment": -0.1912
    }
  ],
  "updated_at": "2026-03-30T08:00:00+00:00"
}
```

### GET /alerts

Return active alert objects.

Response shape:

```json
{
  "alerts": [
    {
      "id": "a3f2...",
      "region": "CA-LA",
      "score": 0.8123,
      "status": "review_required",
      "confidence": 0.71,
      "sample_size": 24,
      "created_at": "2026-03-30T08:00:00+00:00",
      "updated_at": "2026-03-30T08:00:00+00:00",
      "score_breakdown": {
        "sentiment_intensity": 0.7,
        "volume_spike": 0.6,
        "geo_cluster": 0.9,
        "trend_accel": 0.8,
        "bot_ratio": 0.1,
        "confidence": 0.71
      },
      "evidence_post_ids": ["post_1", "post_2"]
    }
  ]
}
```

### POST /alerts/{alert_id}/ack
### POST /alerts/{alert_id}/dismiss
### POST /alerts/{alert_id}/resolve

Transition an alert status.

Response:

```json
{
  "alert": {
    "id": "a3f2...",
    "status": "acknowledged"
  }
}
```

Failure:

- `404` if the alert does not exist

Examples:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/alerts/<alert-id>/ack"
curl -X POST "http://127.0.0.1:8000/api/v1/alerts/<alert-id>/dismiss"
curl -X POST "http://127.0.0.1:8000/api/v1/alerts/<alert-id>/resolve"
```

### GET /logs

Return recent log events.

Query parameters:

- `limit` (`int`, optional, default `100`)

Response shape:

```json
{
  "logs": [
    {
      "timestamp": "2026-03-30T08:00:00+00:00",
      "event": "ingest_completed",
      "payload": {
        "n": 30,
        "total_posts": 125,
        "regions": 9
      }
    }
  ]
}
```

### GET /bias

Return bias-monitoring diagnostics by population tier and by region.

Response fields:

- `by_tier`: aggregated diagnostics grouped into `rural`, `suburban`, `urban`
- `by_region`: per-region diagnostics
- `notes`: operator guidance strings
- `as_of`: timestamp added by the route handler

Example:

```bash
curl "http://127.0.0.1:8000/api/v1/bias"
```
