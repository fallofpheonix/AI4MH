"""
AI4MH — FastAPI Backend
Run: uvicorn main:app --reload --port 8000

Endpoints consumed by the React dashboard:
  GET  /api/posts          — latest ingested posts (NLP-enriched)
  GET  /api/scores         — per-region crisis scores
  GET  /api/alerts         — alert queue
  POST /api/alerts/{id}/review — analyst review action
  GET  /api/audit          — full audit log
  POST /api/ingest         — trigger a new ingestion batch
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime

from ingest_posts      import generate_dataset
from nlp_processing    import analyze_batch
from crisis_scoring    import score_all_regions
from governance_filters import apply_governance
from alert_engine      import evaluate_region, review_alert, get_alerts, get_audit_log

app = FastAPI(title="AI4MH Crisis Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory state (swap for PostgreSQL in production) ───────────────────────
_posts:  list[dict] = []
_scores: list[dict] = []


def _refresh(n: int = 50):
    """Ingest n new posts, re-score all regions."""
    global _posts, _scores
    new_raw  = generate_dataset(n)
    enriched = analyze_batch(new_raw)
    _posts   = (enriched + _posts)[:500]   # keep latest 500

    raw_scores = score_all_regions(_posts)
    _scores    = [apply_governance(s) for s in raw_scores]

    # Evaluate each region for alerts
    for s in _scores:
        evaluate_region(s)


# Seed on startup
@app.on_event("startup")
def startup():
    _refresh(200)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/posts")
def get_posts(limit: int = 50):
    return {"posts": _posts[:limit], "total": len(_posts)}


@app.get("/api/scores")
def get_scores():
    return {"scores": _scores, "updated_at": datetime.datetime.utcnow().isoformat()}


@app.get("/api/alerts")
def get_alerts_route(status: str = None):
    return {"alerts": get_alerts(status)}


class ReviewPayload(BaseModel):
    decision: str   # confirmed | dismissed | monitoring
    analyst:  str = "analyst"
    note:     str = ""

@app.post("/api/alerts/{alert_id}/review")
def review(alert_id: str, payload: ReviewPayload):
    result = review_alert(alert_id, payload.decision, payload.analyst, payload.note)
    return result


@app.get("/api/audit")
def audit():
    return {"log": get_audit_log()}


@app.post("/api/ingest")
def ingest(n: int = 30):
    _refresh(n)
    return {"message": f"Ingested {n} posts", "total_posts": len(_posts), "regions_scored": len(_scores)}
