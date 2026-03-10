"""
AI4MH — Alert Engine
Generates alerts for human review. Never triggers interventions directly.
"""

import uuid, datetime, json, pathlib

ALERT_THRESHOLDS = {
    "final_score": 0.70,
    "confidence":  0.60,
}

_alert_store: list[dict] = []
_audit_log:   list[dict] = []


def _log(entry: dict):
    entry["logged_at"] = datetime.datetime.utcnow().isoformat()
    _audit_log.append(entry)


def evaluate_region(governed: dict) -> dict | None:
    """
    Returns an alert dict if thresholds are met, else None.
    All alerts go to human review — no automatic intervention.
    """
    score = governed.get("final_score", 0)
    conf  = governed.get("confidence", 0)
    ok    = governed.get("governance_ok", False)

    should_alert = (
        score >= ALERT_THRESHOLDS["final_score"] and
        conf  >= ALERT_THRESHOLDS["confidence"]  and
        ok
    )

    _log({
        "event":       "score_evaluated",
        "region_id":   governed["region_id"],
        "final_score": score,
        "confidence":  conf,
        "governance_ok": ok,
        "alert_generated": should_alert,
    })

    if not should_alert:
        return None

    alert = {
        "id":          str(uuid.uuid4())[:12],
        "region_id":   governed["region_id"],
        "final_score": score,
        "confidence":  conf,
        "post_count":  governed["post_count"],
        "bot_ratio":   governed["bot_ratio"],
        "tier":        governed["population_tier"],
        "created_at":  datetime.datetime.utcnow().isoformat(),
        "status":      "pending",   # pending | confirmed | dismissed | monitoring
        "reviewed_by": None,
        "review_note": None,
    }
    _alert_store.append(alert)
    _log({"event": "alert_created", **alert})
    return alert


def review_alert(alert_id: str, decision: str, analyst: str = "analyst", note: str = "") -> dict:
    """
    Human analyst reviews an alert.
    decision: 'confirmed' | 'dismissed' | 'monitoring'
    """
    for alert in _alert_store:
        if alert["id"] == alert_id:
            alert["status"]      = decision
            alert["reviewed_by"] = analyst
            alert["review_note"] = note
            alert["reviewed_at"] = datetime.datetime.utcnow().isoformat()
            _log({"event": "alert_reviewed", "alert_id": alert_id, "decision": decision, "analyst": analyst})
            return alert
    return {"error": f"Alert {alert_id} not found"}


def get_alerts(status: str = None) -> list[dict]:
    if status:
        return [a for a in _alert_store if a["status"] == status]
    return list(_alert_store)


def get_audit_log() -> list[dict]:
    return list(_audit_log)


def save_outputs(out_dir: str = "data"):
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    with open(f"{out_dir}/alerts.json", "w") as f:
        json.dump(_alert_store, f, indent=2)
    with open(f"{out_dir}/audit_log.json", "w") as f:
        json.dump(_audit_log, f, indent=2)
    print(f"Saved {len(_alert_store)} alerts and {len(_audit_log)} audit events.")
