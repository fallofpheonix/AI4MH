# API

Base path: `/api/v1`

## `POST /ingest`

Generate and process a synthetic batch.

Query parameters:

- `n` integer, optional, default `30`

Response:

```json
{
  "total_posts": 125,
  "regions_scored": 9,
  "alerts": 2
}
```

## `GET /posts`

Return recent enriched posts.

Query parameters:

- `limit` integer, optional, default `60`

Response shape:

```json
{
  "posts": [
    {
      "id": "post_123456",
      "text": "thinking about suicide, no way out",
      "subreddit": "SuicideWatch",
      "region_id": "CA-LA",
      "region_name": "Los Angeles, CA",
      "timestamp": "2026-03-31T10:00:00+00:00",
      "upvotes": 14,
      "comments": 8,
      "is_bot": false,
      "is_crisis_text": true,
      "ground_truth_crisis": true,
      "sentiment": -0.82,
      "keyword_count": 2,
      "keyword_terms": ["suicide", "no way out"],
      "nlp_crisis_flag": true,
      "ai_correct": true
    }
  ],
  "total": 125
}
```

## `GET /scores`

Return current regional scores.

Response shape:

```json
{
  "scores": [
    {
      "region_id": "CA-LA",
      "post_count": 25,
      "bot_count": 2,
      "bot_ratio": 0.0741,
      "sentiment_intensity": 0.68,
      "volume_spike": 0.92,
      "geo_cluster": 0.56,
      "trend_accel": 0.71,
      "crisis_score": 0.7365,
      "confidence": 0.625,
      "should_escalate": true,
      "avg_sentiment": -0.43
    }
  ],
  "updated_at": "2026-03-31T10:00:00+00:00"
}
```

## `GET /alerts`

Return current alerts.

Response shape:

```json
{
  "alerts": [
    {
      "id": "uuid",
      "region": "CA-LA",
      "score": 0.81,
      "status": "review_required",
      "confidence": 0.66,
      "sample_size": 25,
      "created_at": "2026-03-31T10:00:00+00:00",
      "updated_at": "2026-03-31T10:00:00+00:00",
      "score_breakdown": {},
      "evidence_post_ids": ["post_123456"]
    }
  ]
}
```

## `POST /alerts/{alert_id}/ack`

Transition alert status to `acknowledged`.

## `POST /alerts/{alert_id}/dismiss`

Transition alert status to `dismissed`.

## `POST /alerts/{alert_id}/resolve`

Transition alert status to `resolved`.

Transition response shape:

```json
{
  "alert": {
    "id": "uuid",
    "region": "CA-LA",
    "status": "acknowledged"
  }
}
```

Unknown alert IDs return `404`.

## `GET /logs`

Return recent log events.

Query parameters:

- `limit` integer, optional, default `100`

Response shape:

```json
{
  "logs": [
    {
      "timestamp": "2026-03-31T10:00:00+00:00",
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

## `GET /bias`

Return population-tier and region-level summary metrics.

Response shape:

```json
{
  "by_tier": {
    "urban": {
      "regions": 4,
      "avg_post_count": 20.5,
      "avg_crisis_score": 0.61,
      "avg_confidence": 0.54,
      "alert_rate": 0.25,
      "low_sample_rate": 0.0
    }
  },
  "by_region": [],
  "notes": [],
  "as_of": "2026-03-31T10:00:00+00:00"
}
```
