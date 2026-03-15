"""
AI4MH Backend (FastAPI)

Defines all HTTP routes and delegates work to the pipeline and storage layers.
No pipeline logic lives here — this file only wires routes to functions.

Endpoints:
- POST /api/ingest
- GET  /api/posts
- GET  /api/scores
- GET  /api/alerts
- POST /api/alerts/{id}/ack
- POST /api/alerts/{id}/dismiss
- POST /api/alerts/{id}/resolve
- GET  /api/logs
- GET  /api/bias
"""

from __future__ import annotations

import datetime
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models.alert import Alert, LogEvent
from pipeline.aggregate import group_by_region
from pipeline.alert import generate_alerts
from pipeline.enrich import enrich_batch
from pipeline.ingest import REGIONS, generate_dataset
from pipeline.score import score_all_regions
from storage.memory import MemoryStore

app = FastAPI(title="AI4MH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single storage instance — replace with a different Store subclass to swap
# backends (e.g. RedisStore, SQLiteStore).
_store = MemoryStore(max_posts=settings.max_posts)

_region_population: dict[str, int] = {r["id"]: r["population"] for r in REGIONS}


# ------------------------------------------------------------------ helpers


def _population_tier(region_id: str) -> str:
    """Map a region to its population tier label."""
    pop = _region_population.get(region_id, 500_000)
    if pop < 100_000:
        return "rural"
    if pop < 1_000_000:
        return "suburban"
    return "urban"


def _run_pipeline(n: int = 30) -> None:
    """
    Execute one full ingest → enrich → score → alert cycle.

    Only regions affected by the new posts have their scores recomputed.
    """
    try:
        raw_posts = generate_dataset(n)
        enriched = enrich_batch(raw_posts)

        # Determine which regions were touched in this batch.
        new_region_ids = {p.region_id for p in enriched}

        _store.save_posts(enriched)

        all_posts = _store.get_posts()
        existing_scores = _store.get_scores()

        scores = score_all_regions(
            all_posts,
            affected_regions=new_region_ids,
            existing_scores=existing_scores,
        )
        _store.save_scores(scores)

        region_posts = group_by_region(all_posts)
        existing_alerts = _store.get_alerts()
        new_alerts, alert_logs = generate_alerts(scores, existing_alerts, region_posts)
        _store.save_alerts(new_alerts)

        for log_event in alert_logs:
            _store.append_log(log_event)

        _store.append_log(
            LogEvent(
                event="ingest_completed",
                payload={
                    "n": n,
                    "total_posts": len(all_posts),
                    "regions": len(scores),
                },
            )
        )
    except Exception as exc:
        _store.append_log(
            LogEvent(
                event="ingest_error",
                payload={"error": str(exc)},
            )
        )
        raise


# ------------------------------------------------------------------ startup


@app.on_event("startup")
def startup() -> None:
    _run_pipeline(120)


# ------------------------------------------------------------------ routes


@app.get("/api/posts")
def get_posts(limit: int = 60):
    posts = _store.get_posts(limit=limit)
    return {"posts": [p.model_dump() for p in posts], "total": len(_store.get_posts())}


@app.get("/api/scores")
def get_scores():
    scores = _store.get_scores()
    return {
        "scores": [s.model_dump() for s in scores],
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


@app.get("/api/alerts")
def get_alerts():
    alerts = _store.get_alerts()
    return {"alerts": [a.model_dump() for a in alerts]}


@app.post("/api/alerts/{alert_id}/ack")
def ack_alert(alert_id: str):
    """Acknowledge an alert — moves it from *review_required* to *acknowledged*."""
    return _transition_alert(alert_id, "acknowledged")


@app.post("/api/alerts/{alert_id}/dismiss")
def dismiss_alert(alert_id: str):
    """Dismiss an alert — operator has reviewed and deemed it a false positive."""
    return _transition_alert(alert_id, "dismissed")


@app.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    """Resolve an alert — crisis has been addressed or escalated externally."""
    return _transition_alert(alert_id, "resolved")


def _transition_alert(alert_id: str, new_status: str) -> dict:
    """Apply a lifecycle transition to an alert and persist the change."""
    alert = _store.get_alert(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found.")
    updated = alert.model_copy(
        update={
            "status": new_status,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    )
    _store.update_alert(updated)
    _store.append_log(
        LogEvent(
            event="alert_status_changed",
            payload={"alert_id": alert_id, "new_status": new_status},
        )
    )
    return {"alert": updated.model_dump()}


@app.get("/api/logs")
def get_logs(limit: int = 100):
    logs = _store.get_logs(limit=limit)
    return {"logs": [e.model_dump() for e in logs]}


@app.get("/api/bias")
def get_bias_diagnostics():
    """
    Group-level diagnostics for bias monitoring.

    This endpoint does not claim fairness compliance; it provides
    transparent indicators to detect systematic regional skew.
    """
    scores = _store.get_scores()
    alerts = _store.get_alerts()

    score_by_region = {s.region_id: s for s in scores}
    alert_regions = {a.region for a in alerts}

    by_region = []
    grouped: dict[str, list[dict]] = defaultdict(list)
    for region_id, score in score_by_region.items():
        row = {
            "region_id": region_id,
            "population_tier": _population_tier(region_id),
            "post_count": score.post_count,
            "crisis_score": score.crisis_score,
            "confidence": score.confidence,
            "alert_flag": region_id in alert_regions,
            "low_sample_flag": score.post_count < 20,
        }
        by_region.append(row)
        grouped[row["population_tier"]].append(row)

    by_tier = {}
    for tier, rows in grouped.items():
        n = len(rows)
        n_alerts = sum(1 for r in rows if r["alert_flag"])
        by_tier[tier] = {
            "regions": n,
            "avg_post_count": round(
                sum(r["post_count"] for r in rows) / max(n, 1), 4
            ),
            "avg_crisis_score": round(
                sum(r["crisis_score"] for r in rows) / max(n, 1), 4
            ),
            "avg_confidence": round(
                sum(r["confidence"] for r in rows) / max(n, 1), 4
            ),
            "alert_rate": round(n_alerts / max(n, 1), 4),
            "low_sample_rate": round(
                sum(1 for r in rows if r["low_sample_flag"]) / max(n, 1), 4
            ),
        }

    return {
        "as_of": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "by_tier": by_tier,
        "by_region": by_region,
        "notes": [
            "Use these diagnostics for drift/skew detection across population tiers.",
            "Human review remains mandatory for operational escalation decisions.",
        ],
    }


@app.post("/api/ingest")
def ingest(n: int = 30):
    """Run one ingest cycle synchronously and return a summary."""
    _run_pipeline(n)
    all_posts = _store.get_posts()
    scores = _store.get_scores()
    alerts = _store.get_alerts()
    return {
        "message": f"Ingested {n} posts",
        "total_posts": len(all_posts),
        "regions_scored": len(scores),
        "alerts": len(alerts),
    }
