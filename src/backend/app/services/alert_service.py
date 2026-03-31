from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.config import settings
from app.crud.base import Store
from app.schemas.alert import Alert, LogEvent
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore


class AlertService:
    def __init__(self, store: Store) -> None:
        self._store = store

    def rebuild_alerts(
        self,
        scores: list[RegionScore],
        region_posts: dict[str, list[EnrichedPost]],
    ) -> list[LogEvent]:
        current_alerts = self._store.get_alerts()
        current_by_region = {alert.region: alert for alert in current_alerts}
        next_alerts: list[Alert] = []
        log_events: list[LogEvent] = []

        for score in scores:
            if score.crisis_score <= settings.alert_threshold:
                continue

            evidence_ids = [post.id for post in region_posts.get(score.region_id, []) if post.nlp_crisis_flag]
            existing = current_by_region.get(score.region_id)
            if existing is not None and existing.status != "review_required":
                next_alerts.append(
                    existing.model_copy(
                        update={
                            "score": round(score.crisis_score, 4),
                            "confidence": score.confidence,
                            "sample_size": score.post_count,
                            "updated_at": self._now(),
                            "score_breakdown": self._breakdown(score),
                            "evidence_post_ids": evidence_ids,
                        }
                    )
                )
                continue

            next_alerts.append(
                Alert(
                    region=score.region_id,
                    score=round(score.crisis_score, 4),
                    confidence=score.confidence,
                    sample_size=score.post_count,
                    score_breakdown=self._breakdown(score),
                    evidence_post_ids=evidence_ids,
                )
            )
            log_events.append(
                LogEvent(
                    event="alert_generated",
                    payload={
                        "region": score.region_id,
                        "score": round(score.crisis_score, 4),
                        "confidence": score.confidence,
                        "sample_size": score.post_count,
                    },
                )
            )

        scored_regions = {score.region_id for score in scores}
        for alert in current_alerts:
            if alert.region not in scored_regions and alert.status != "review_required":
                next_alerts.append(alert)

        self._store.save_alerts(next_alerts)
        return log_events

    def transition(self, alert_id: str, new_status: str) -> Alert:
        alert = self._store.get_alert(alert_id)
        if alert is None:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found.")

        updated = alert.model_copy(update={"status": new_status, "updated_at": self._now()})
        self._store.update_alert(updated)
        self._store.append_log(
            LogEvent(
                event="alert_status_changed",
                payload={"alert_id": alert_id, "new_status": new_status},
            )
        )
        return updated

    def list_alerts(self) -> list[Alert]:
        return self._store.get_alerts()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _breakdown(score: RegionScore) -> dict[str, float]:
        return {
            "sentiment_intensity": score.sentiment_intensity,
            "volume_spike": score.volume_spike,
            "geo_cluster": score.geo_cluster,
            "trend_accel": score.trend_accel,
            "bot_ratio": score.bot_ratio,
            "confidence": score.confidence,
        }
