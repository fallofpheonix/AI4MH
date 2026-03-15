"""
AI4MH — Alert Generation Pipeline Stage

Converts region score snapshots into actionable alerts and manages their
lifecycle states. This module has no FastAPI dependency.
"""

from __future__ import annotations

import datetime
import logging
from typing import List

from config import settings
from models.alert import Alert, LogEvent
from models.score import RegionScore

logger = logging.getLogger(__name__)


def generate_alerts(
    scores: List[RegionScore],
    existing_alerts: List[Alert],
    region_posts: dict,
) -> tuple[List[Alert], List[LogEvent]]:
    """
    Generate fresh alerts from a new score snapshot.

    Existing alerts that are no longer above threshold are removed.
    Acknowledged / dismissed / resolved alerts are preserved even if
    the region has dropped below the threshold.

    Parameters
    ----------
    scores:
        Current region score snapshot.
    existing_alerts:
        Alerts from the previous pipeline cycle.
    region_posts:
        Mapping of region_id → list of EnrichedPost (for evidence linking).

    Returns
    -------
    (alerts, log_events)
    """
    threshold = settings.alert_threshold
    logs: List[LogEvent] = []

    # Index existing alerts by region for fast lookup.
    existing_by_region: dict[str, Alert] = {a.region: a for a in existing_alerts}

    new_alerts: List[Alert] = []

    for region_score in scores:
        crisis_score = region_score.crisis_score

        if crisis_score > threshold:
            posts = region_posts.get(region_score.region_id, [])
            evidence_ids = [p.id for p in posts if p.nlp_crisis_flag]

            existing = existing_by_region.get(region_score.region_id)
            if existing and existing.status != "review_required":
                # Preserve non-default lifecycle state.
                updated = existing.model_copy(
                    update={
                        "score": round(crisis_score, 4),
                        "confidence": region_score.confidence,
                        "sample_size": region_score.post_count,
                        "updated_at": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat(),
                        "score_breakdown": _breakdown(region_score),
                        "evidence_post_ids": evidence_ids,
                    }
                )
                new_alerts.append(updated)
            else:
                alert = Alert(
                    region=region_score.region_id,
                    score=round(crisis_score, 4),
                    status="review_required",
                    confidence=region_score.confidence,
                    sample_size=region_score.post_count,
                    score_breakdown=_breakdown(region_score),
                    evidence_post_ids=evidence_ids,
                )
                new_alerts.append(alert)
                logs.append(
                    LogEvent(
                        event="alert_generated",
                        payload={
                            "region": region_score.region_id,
                            "score": round(crisis_score, 4),
                            "confidence": region_score.confidence,
                            "sample_size": region_score.post_count,
                        },
                    )
                )

    # Preserve manually updated alerts for regions no longer above threshold.
    score_regions = {s.region_id for s in scores}
    for alert in existing_alerts:
        if alert.region not in score_regions and alert.status != "review_required":
            new_alerts.append(alert)

    return new_alerts, logs


def _breakdown(score: RegionScore) -> dict:
    """Return a human-readable scoring breakdown dict for an alert."""
    return {
        "sentiment_intensity": score.sentiment_intensity,
        "volume_spike": score.volume_spike,
        "geo_cluster": score.geo_cluster,
        "trend_accel": score.trend_accel,
        "bot_ratio": score.bot_ratio,
        "confidence": score.confidence,
    }
