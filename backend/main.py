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
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import datetime
import csv
import io

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


def _select_export_rows(kind: str) -> list[dict]:
    if kind == "posts":
        return _posts
    if kind == "scores":
        return _scores
    if kind == "alerts":
        return get_alerts()
    if kind == "audit":
        return get_audit_log()
    raise ValueError(f"Unsupported export kind: {kind}")


def _to_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    fields = sorted({k for r in rows for k in r.keys()})
    buff = io.StringIO()
    writer = csv.DictWriter(buff, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, "") for k in fields})
    return buff.getvalue()


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


@app.get("/api/export/json")
def export_json(kind: str = "posts"):
    rows = _select_export_rows(kind)
    return {"kind": kind, "rows": rows, "count": len(rows), "exported_at": datetime.datetime.utcnow().isoformat()}


@app.get("/api/export/csv", response_class=PlainTextResponse)
def export_csv(kind: str = "posts"):
    rows = _select_export_rows(kind)
    return _to_csv(rows)
