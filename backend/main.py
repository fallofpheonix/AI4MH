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


@app.post("/api/ingest")
def ingest(n: int = 30):
    _refresh(n)
    return {
        "message": f"Ingested {n} posts",
        "total_posts": len(_posts),
        "regions_scored": len(_scores),
        "alerts": len(_alerts),
    }
