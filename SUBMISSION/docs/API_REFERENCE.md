# API Reference

Complete API documentation for AI4MH backend endpoints.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently no authentication (would be added in Phase 2).
All endpoints are public.

## Response Format

All responses are JSON with the following structure:

```json
{
  "data": {...},
  "status": "success|error",
  "timestamp": "2024-03-17T12:00:00Z"
}
```

Successful responses return HTTP 200 (or specific 201, 204).  
Error responses return appropriate HTTP 4xx or 5xx status codes.

---

## Endpoints

### Posts

#### GET /api/posts

Retrieve recent posts with optional limit.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| limit | integer | No | 60 | Number of posts to return |

**Response:**
```json
{
  "posts": [
    {
      "id": "post_123",
      "text": "I am feeling overwhelmed",
      "region_id": "AL",
      "sentiment_compound": -0.7,
      "crisis_keywords": 1,
      "created_at": "2024-03-17T12:00:00Z"
    }
  ],
  "total": 150
}
```

**Status Codes:**
- 200: Success
- 400: Invalid limit parameter
- 500: Server error

**Example:**
```bash
curl http://localhost:8000/api/posts?limit=10
```

---

### Scores

#### GET /api/scores

Get regional crisis scores for all regions.

**Parameters:** None

**Response:**
```json
{
  "scores": [
    {
      "region_id": "AL",
      "crisis_score": 0.82,
      "confidence": 0.91,
      "components": {
        "sentiment": 0.75,
        "volume": 0.88,
        "geo_cluster": 0.80,
        "trend": 0.70
      },
      "num_posts": 125,
      "baseline_posts": 45,
      "updated_at": "2024-03-17T12:30:00Z"
    }
  ],
  "updated_at": "2024-03-17T12:30:00Z"
}
```

**Status Codes:**
- 200: Success
- 500: Server error

**Example:**
```bash
curl http://localhost:8000/api/scores
```

---

### Alerts

#### GET /api/alerts

List all alerts with optional filtering.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| status | string | No | all | Filter by status (review_required, acknowledged, dismissed, resolved) |
| region_id | string | No | all | Filter by region |
| limit | integer | No | 50 | Number of alerts to return |

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert_456",
      "region_id": "AL",
      "crisis_score": 0.85,
      "confidence": 0.92,
      "status": "review_required",
      "evidence_post_ids": ["post_1", "post_2", "post_3"],
      "score_breakdown": {
        "sentiment": 0.80,
        "volume": 0.90,
        "geo_cluster": 0.82,
        "trend": 0.72
      },
      "created_at": "2024-03-17T12:00:00Z",
      "updated_at": "2024-03-17T12:00:00Z",
      "acknowledged_at": null,
      "resolved_at": null
    }
  ],
  "total": 5
}
```

**Status Codes:**
- 200: Success
- 400: Invalid status or region_id parameter
- 500: Server error

**Example:**
```bash
curl http://localhost:8000/api/alerts?status=review_required&region_id=AL
```

---

#### POST /api/alerts/{id}/ack

Acknowledge an alert (transition from review_required → acknowledged).

**Parameters:**
- `id` (path parameter): Alert ID

**Request Body:**
```json
{
  "notes": "Alert reviewed. Investigating further."
}
```

**Response:**
```json
{
  "alert": {
    "id": "alert_456",
    "status": "acknowledged",
    "acknowledged_at": "2024-03-17T12:15:00Z",
    "acknowledged_by": "operator_1",
    "notes": "Alert reviewed. Investigating further."
  }
}
```

**Status Codes:**
- 200: Success
- 404: Alert not found
- 409: Alert not in review_required state
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:8000/api/alerts/alert_456/ack \
  -H "Content-Type: application/json" \
  -d '{"notes": "Investigating"}'
```

---

#### POST /api/alerts/{id}/dismiss

Dismiss an alert (transition from review_required → dismissed).

**Parameters:**
- `id` (path parameter): Alert ID

**Request Body:**
```json
{
  "reason": "False positive - unrelated discussion spike",
  "notes": "Media coverage about similar issue"
}
```

**Response:**
```json
{
  "alert": {
    "id": "alert_456",
    "status": "dismissed",
    "dismissed_at": "2024-03-17T12:20:00Z",
    "reason": "False positive - unrelated discussion spike"
  }
}
```

**Status Codes:**
- 200: Success
- 404: Alert not found
- 409: Alert not in review_required state
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:8000/api/alerts/alert_456/dismiss \
  -H "Content-Type: application/json" \
  -d '{"reason": "False positive", "notes": "Media coverage"}'
```

---

#### POST /api/alerts/{id}/resolve

Resolve an alert (transition from acknowledged → resolved).

**Parameters:**
- `id` (path parameter): Alert ID

**Request Body:**
```json
{
  "outcome": "Crisis identified and addressed",
  "actions_taken": "Contacted regional mental health center"
}
```

**Response:**
```json
{
  "alert": {
    "id": "alert_456",
    "status": "resolved",
    "resolved_at": "2024-03-17T12:45:00Z",
    "outcome": "Crisis identified and addressed",
    "actions_taken": "Contacted regional mental health center"
  }
}
```

**Status Codes:**
- 200: Success
- 404: Alert not found
- 409: Alert not in acknowledged state
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:8000/api/alerts/alert_456/resolve \
  -H "Content-Type: application/json" \
  -d '{"outcome": "Resolved", "actions_taken": "Contacted center"}'
```

---

### Logs

#### GET /api/logs

Retrieve audit logs for system events.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| event | string | No | all | Filter by event type |
| limit | integer | No | 20 | Number of log entries to return |
| offset | integer | No | 0 | Pagination offset |

**Response:**
```json
{
  "logs": [
    {
      "id": "log_789",
      "event": "ingest_completed",
      "timestamp": "2024-03-17T12:30:00Z",
      "payload": {
        "n": 30,
        "total_posts": 1250,
        "regions": 5
      }
    },
    {
      "id": "log_788",
      "event": "alert_acknowledged",
      "timestamp": "2024-03-17T12:15:00Z",
      "payload": {
        "alert_id": "alert_456",
        "region": "AL",
        "crisis_score": 0.85
      }
    }
  ],
  "total": 245
}
```

**Event Types:**
- `ingest_completed` - Data ingestion cycle completed
- `ingest_error` - Error during ingestion
- `alert_escalated` - Alert generated and marked as review_required
- `alert_acknowledged` - Alert acknowledged by operator
- `alert_dismissed` - Alert dismissed by operator
- `alert_resolved` - Alert resolved by operator

**Status Codes:**
- 200: Success
- 400: Invalid event type or limit
- 500: Server error

**Example:**
```bash
curl http://localhost:8000/api/logs?event=alert_escalated&limit=10
```

---

### Bias Diagnostics

#### GET /api/bias

Get bias diagnostics for data quality assessment.

**Parameters:** None

**Response:**
```json
{
  "by_tier": {
    "rural": {
      "regions": 2,
      "avg_posts": 8,
      "warning": "Low sample size (N=8) - use with caution"
    },
    "suburban": {
      "regions": 5,
      "avg_posts": 45,
      "warning": null
    },
    "urban": {
      "regions": 3,
      "avg_posts": 250,
      "warning": null
    }
  },
  "by_region": [
    {
      "region_id": "AL_rural_1",
      "population_tier": "rural",
      "posts": 5,
      "confidence": 0.45,
      "bot_ratio": 0.2,
      "recommendation": "Increase confidence threshold for this region"
    }
  ],
  "global_stats": {
    "total_posts": 1250,
    "low_sample_regions": 2,
    "high_bot_regions": 1
  }
}
```

**Status Codes:**
- 200: Success
- 500: Server error

**Example:**
```bash
curl http://localhost:8000/api/bias
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "status": 400
}
```

### Common Errors

| Status | Message | Cause |
|--------|---------|-------|
| 400 | Bad Request | Invalid parameters or request body |
| 404 | Not Found | Resource (alert, post) doesn't exist |
| 409 | Conflict | Invalid state transition (e.g., resolve dismissed alert) |
| 500 | Internal Server Error | Unexpected server error |

---

## Rate Limiting

Currently no rate limiting implemented.
Can be added in Phase 2:

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/posts")
@limiter.limit("100/minute")
def get_posts():
    ...
```

---

## Pagination

Use `limit` and `offset` parameters for large result sets:

```bash
# Get first 20 items
curl http://localhost:8000/api/posts?limit=20&offset=0

# Get next 20 items
curl http://localhost:8000/api/posts?limit=20&offset=20
```

---

## Filtering

### By Status
```bash
curl http://localhost:8000/api/alerts?status=review_required
```

### By Region
```bash
curl http://localhost:8000/api/alerts?region_id=AL
```

### Combined
```bash
curl http://localhost:8000/api/alerts?status=acknowledged&region_id=GA
```

---

## Testing Endpoints

### Using curl

```bash
# Test backend health
curl -i http://localhost:8000/api/posts

# Test with jq for pretty JSON
curl -s http://localhost:8000/api/scores | jq '.'

# POST request
curl -X POST http://localhost:8000/api/alerts/alert_456/ack \
  -H "Content-Type: application/json" \
  -d '{"notes": "Reviewing"}'
```

### Using Python

```python
import requests

# Get posts
response = requests.get('http://localhost:8000/api/posts?limit=5')
posts = response.json()['posts']

# Get scores
scores = requests.get('http://localhost:8000/api/scores').json()['scores']

# Acknowledge alert
requests.post(
    'http://localhost:8000/api/alerts/alert_456/ack',
    json={"notes": "Reviewing..."}
)
```

### Using JavaScript/Fetch

```javascript
// Get posts
fetch('http://localhost:8000/api/posts?limit=5')
  .then(r => r.json())
  .then(data => console.log(data.posts));

// Acknowledge alert
fetch('http://localhost:8000/api/alerts/alert_456/ack', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ notes: 'Reviewing' })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## OpenAPI/Swagger

Interactive API documentation available at:

```
http://localhost:8000/docs
```

Alternative (ReDoc):
```
http://localhost:8000/redoc
```

---

## Versioning

Current API version: `v1`  
No version prefix currently used in endpoints.

For future versions, use:
```
/api/v2/posts
/api/v2/scores
```

---

## CORS

The following origins are allowed:
- `http://localhost:3000`
- `http://localhost:5173`

Add more in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    ...
)
```

---

## Metrics & Monitoring

### Response Times

Typical response times:
- GET endpoints: 50-100ms
- POST endpoints: 100-200ms
- Complex queries (bias): 200-500ms

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/posts

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/posts
```

---

## Support & Issues

For API issues:
1. Check [SUBMISSION/docs/GOVERNANCE.md](GOVERNANCE.md) for governance questions
2. Review error logs: `docker logs ai4mh-backend`
3. Consult [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) for design questions

---

**API Reference Last Updated:** March 17, 2026  
**Status:** Production Ready ✅
