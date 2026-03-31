# API Reference

Base path: `/api/v1`

All requests and responses use JSON. Successful responses return HTTP `200` unless noted. Error responses return a JSON body with a `detail` field.

## `POST /ingest`

Generate and process a synthetic batch of posts through the full pipeline.

Query parameters:

| Name | Type | Default | Description |
|---|---|---|---|
| `n` | integer | `30` | Number of synthetic posts to generate |

Response `200`:

```json
{
  "total_posts": 125,
  "regions_scored": 9,
  "alerts": 2
}
```

## `GET /posts`

Return recent enriched posts ordered by ingestion recency (newest first).

Query parameters:

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | integer | `60` | Maximum number of posts to return |

Response `200`:

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

Return the current set of regional crisis scores, sorted by `crisis_score` descending.

Response `200`:

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

Return all current alerts (any status).

Response `200`:

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
      "score_breakdown": {
        "sentiment_intensity": 0.68,
        "volume_spike": 0.92,
        "geo_cluster": 0.56,
        "trend_accel": 0.71,
        "bot_ratio": 0.0741,
        "confidence": 0.625
      },
      "evidence_post_ids": ["post_123456"]
    }
  ]
}
```

Alert status values: `review_required` | `acknowledged` | `dismissed` | `resolved`

## `POST /alerts/{alert_id}/ack`

Transition alert status to `acknowledged`.

Path parameters:

| Name | Type | Description |
|---|---|---|
| `alert_id` | string (UUID) | ID of the alert to acknowledge |

Response `200`:

```json
{
  "alert": {
    "id": "uuid",
    "region": "CA-LA",
    "status": "acknowledged"
  }
}
```

Errors:

| Status | Condition |
|---|---|
| `404` | No alert with the given ID exists |

## `POST /alerts/{alert_id}/dismiss`

Transition alert status to `dismissed`.

Path and error behaviour identical to `/ack`.

## `POST /alerts/{alert_id}/resolve`

Transition alert status to `resolved`.

Path and error behaviour identical to `/ack`.

## `GET /logs`

Return recent pipeline log events ordered by event time ascending.

Query parameters:

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | integer | `100` | Maximum number of events to return |

Response `200`:

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

Known event types:

| Event | Payload fields | Description |
|---|---|---|
| `ingest_completed` | `n`, `total_posts`, `regions` | Logged after every pipeline cycle |
| `alert_generated` | `region`, `score`, `confidence`, `sample_size` | Logged when a new alert is created |
| `alert_status_changed` | `alert_id`, `new_status` | Logged on every status transition |

## `GET /bias`

Return population-tier and region-level summary metrics for fairness review.

Response `200`:

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
    },
    "suburban": { "...": "..." },
    "rural": { "...": "..." }
  },
  "by_region": [
    {
      "region_id": "CA-LA",
      "population_tier": "urban",
      "post_count": 25,
      "crisis_score": 0.74,
      "confidence": 0.63,
      "alert_flag": true,
      "low_sample_flag": false
    }
  ],
  "notes": [
    "These numbers are guardrails, not proof of fairness.",
    "Operators should treat low-volume regions with extra skepticism."
  ],
  "as_of": "2026-03-31T10:00:00+00:00"
}
```

Population tiers: `rural` (< 100 k), `suburban` (100 k – 1 M), `urban` (≥ 1 M).
