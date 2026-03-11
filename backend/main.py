"""
AI4MH Minimal Backend (FastAPI)
Strict MVP scope:
- POST /api/ingest
- GET  /api/posts
- GET  /api/scores
- GET  /api/alerts
- GET  /api/logs
"""

from __future__ import annotations

import datetime
from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ingest_posts import generate_dataset
from ingest_posts import REGIONS
from nlp_processing import analyze_batch
from crisis_scoring import score_all_regions

ALERT_THRESHOLD = 0.75
MAX_POSTS = 500

app = FastAPI(title="AI4MH Minimal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_posts: list[dict] = []
_scores: list[dict] = []
_alerts: list[dict] = []
_logs: list[dict] = []
_region_population: dict[str, int] = {r["id"]: r["population"] for r in REGIONS}


def _log(event: str, payload: dict | None = None) -> None:
    _logs.append(
        {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event": event,
            "payload": payload or {},
        }
    )


def _refresh(n: int = 30) -> None:
    """Ingest n posts, run NLP + scoring, regenerate alerts."""
    global _posts, _scores, _alerts

    raw_posts = generate_dataset(n)
    enriched = analyze_batch(raw_posts)
    _posts = (enriched + _posts)[:MAX_POSTS]

    _scores = score_all_regions(_posts)

    # Minimal alert generation from current region scores.
    _alerts = []
    for region in _scores:
        crisis_score = float(region.get("crisis_score", 0.0))
        if crisis_score > ALERT_THRESHOLD:
            _alerts.append(
                {
                    "region": region.get("region_id"),
                    "score": round(crisis_score, 4),
                    "status": "review_required",
                    "confidence": region.get("confidence"),
                    "sample_size": region.get("post_count"),
                }
            )
            _log(
                "alert_generated",
                {
                    "region": region.get("region_id"),
                    "score": round(crisis_score, 4),
                    "confidence": region.get("confidence"),
                    "sample_size": region.get("post_count"),
                },
            )

    _log("ingest_completed", {"n": n, "total_posts": len(_posts), "regions": len(_scores)})


def _population_tier(region_id: str) -> str:
    pop = _region_population.get(region_id, 500_000)
    if pop < 100_000:
        return "rural"
    if pop < 1_000_000:
        return "suburban"
    return "urban"


@app.on_event("startup")
def startup() -> None:
    _refresh(120)


@app.get("/api/posts")
def get_posts(limit: int = 60):
    return {"posts": _posts[:limit], "total": len(_posts)}


@app.get("/api/scores")
def get_scores():
    return {
        "scores": _scores,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }


@app.get("/api/alerts")
def get_alerts():
    return {"alerts": _alerts}


@app.get("/api/logs")
def get_logs(limit: int = 100):
    return {"logs": _logs[-limit:]}


@app.get("/api/bias")
def get_bias_diagnostics():
    """
    Group-level diagnostics for bias monitoring.
    This endpoint does not claim fairness compliance; it provides
    transparent indicators to detect systematic regional skew.
    """
    score_by_region = {s["region_id"]: s for s in _scores}
    alert_regions = {a["region"] for a in _alerts}

    by_region = []
    grouped: dict[str, list[dict]] = defaultdict(list)
    for region_id, score in score_by_region.items():
        row = {
            "region_id": region_id,
            "population_tier": _population_tier(region_id),
            "post_count": score.get("post_count", 0),
            "crisis_score": score.get("crisis_score", 0.0),
            "confidence": score.get("confidence", 0.0),
            "alert_flag": region_id in alert_regions,
            "low_sample_flag": score.get("post_count", 0) < 20,
        }
        by_region.append(row)
        grouped[row["population_tier"]].append(row)

    by_tier = {}
    for tier, rows in grouped.items():
        n = len(rows)
        alerts = sum(1 for r in rows if r["alert_flag"])
        by_tier[tier] = {
            "regions": n,
            "avg_post_count": round(sum(r["post_count"] for r in rows) / max(n, 1), 4),
            "avg_crisis_score": round(sum(r["crisis_score"] for r in rows) / max(n, 1), 4),
            "avg_confidence": round(sum(r["confidence"] for r in rows) / max(n, 1), 4),
            "alert_rate": round(alerts / max(n, 1), 4),
            "low_sample_rate": round(sum(1 for r in rows if r["low_sample_flag"]) / max(n, 1), 4),
        }

    return {
        "as_of": datetime.datetime.utcnow().isoformat(),
        "by_tier": by_tier,
        "by_region": by_region,
        "notes": [
            "Use these diagnostics for drift/skew detection across population tiers.",
            "Human review remains mandatory for operational escalation decisions.",
        ],
    }


@app.post("/api/ingest")
def ingest(n: int = 30):
    _refresh(n)
    return {
        "message": f"Ingested {n} posts",
        "total_posts": len(_posts),
        "regions_scored": len(_scores),
        "alerts": len(_alerts),
    }
