"""Pipeline service — orchestrates the full ingest → enrich → score → alert cycle."""
from __future__ import annotations

from collections import defaultdict

from app.core.config import settings
from app.crud.base import Store
from app.schemas.alert import LogEvent
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore
from app.services.alert_service import AlertService
from app.services.enrichment_service import EnrichmentService
from app.services.ingestion_service import IngestionService
from app.services.scoring_service import ScoringService
from app.utils.population import classify_population_tier


class PipelineService:
    def __init__(
        self,
        *,
        store: Store,
        ingestion: IngestionService,
        enrichment: EnrichmentService,
        scoring: ScoringService,
        alerts: AlertService,
    ) -> None:
        self._store = store
        self._ingestion = ingestion
        self._enrichment = enrichment
        self._scoring = scoring
        self._alerts = alerts

    def bootstrap(self) -> None:
        if self._store.get_posts(limit=1):
            return
        self.run_cycle(settings.bootstrap_batch_size)

    def run_cycle(self, batch_size: int | None = None) -> dict[str, int]:
        size = batch_size or settings.default_ingest_batch_size
        raw_posts = self._ingestion.build_dataset(size)
        enriched_posts = self._enrichment.enrich_batch(raw_posts)
        affected_regions = {post.region_id for post in enriched_posts}

        self._store.save_posts(enriched_posts)

        all_posts = self._store.get_posts()
        scores = self._scoring.score_regions(
            all_posts,
            affected_regions=affected_regions,
            existing_scores=self._store.get_scores(),
        )
        self._store.save_scores(scores)

        grouped_posts = self._group_posts(all_posts)
        log_events = self._alerts.rebuild_alerts(scores, grouped_posts)
        for event in log_events:
            self._store.append_log(event)

        self._store.append_log(
            LogEvent(
                event="ingest_completed",
                payload={
                    "n": size,
                    "total_posts": len(all_posts),
                    "regions": len(scores),
                },
            )
        )

        return {
            "total_posts": len(all_posts),
            "regions_scored": len(scores),
            "alerts": len(self._store.get_alerts()),
        }

    def list_posts(self, limit: int = 60) -> dict[str, object]:
        posts = self._store.get_posts(limit=limit)
        return {"posts": [post.model_dump() for post in posts], "total": len(self._store.get_posts())}

    def list_scores(self) -> list[RegionScore]:
        return self._store.get_scores()

    def list_logs(self, limit: int = 100) -> list[LogEvent]:
        return self._store.get_logs(limit=limit)

    def build_bias_summary(self) -> dict[str, object]:
        scores = self._store.get_scores()
        alerts = self._store.get_alerts()
        alerted_regions = {alert.region for alert in alerts}

        by_region: list[dict[str, object]] = []
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for score in scores:
            tier = classify_population_tier(self._ingestion.get_population(score.region_id))
            row = {
                "region_id": score.region_id,
                "population_tier": tier,
                "post_count": score.post_count,
                "crisis_score": score.crisis_score,
                "confidence": score.confidence,
                "alert_flag": score.region_id in alerted_regions,
                "low_sample_flag": score.post_count < 20,
            }
            by_region.append(row)
            grouped[tier].append(row)

        by_tier: dict[str, dict[str, float | int]] = {}
        for tier, rows in grouped.items():
            count = len(rows)
            by_tier[tier] = {
                "regions": count,
                "avg_post_count": round(sum(row["post_count"] for row in rows) / max(count, 1), 4),
                "avg_crisis_score": round(sum(row["crisis_score"] for row in rows) / max(count, 1), 4),
                "avg_confidence": round(sum(row["confidence"] for row in rows) / max(count, 1), 4),
                "alert_rate": round(sum(1 for row in rows if row["alert_flag"]) / max(count, 1), 4),
                "low_sample_rate": round(sum(1 for row in rows if row["low_sample_flag"]) / max(count, 1), 4),
            }

        return {
            "by_tier": by_tier,
            "by_region": by_region,
            "notes": [
                "These numbers are guardrails, not proof of fairness.",
                "Operators should treat low-volume regions with extra skepticism.",
            ],
        }

    @staticmethod
    def _group_posts(posts: list[EnrichedPost]) -> dict[str, list[EnrichedPost]]:
        grouped: dict[str, list[EnrichedPost]] = defaultdict(list)
        for post in posts:
            grouped[post.region_id].append(post)
        return dict(grouped)
