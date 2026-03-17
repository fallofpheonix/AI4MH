from __future__ import annotations

from collections import defaultdict

from app.config import settings
from app.core.models.post import EnrichedPost
from app.core.models.score import RegionScore


class ScoringService:
    def score_regions(
        self,
        posts: list[EnrichedPost],
        *,
        affected_regions: set[str] | None = None,
        existing_scores: list[RegionScore] | None = None,
    ) -> list[RegionScore]:
        grouped = self._group_by_region(posts)
        global_average = self._global_average(grouped)

        if affected_regions is None or existing_scores is None:
            scores: list[RegionScore] = []
            for region_id, region_posts in grouped.items():
                region_score = self.score_region(region_id, region_posts, global_average)
                if region_score is not None:
                    scores.append(region_score)
            return sorted(scores, key=lambda item: item.crisis_score, reverse=True)

        score_map = {score.region_id: score for score in existing_scores}
        for region_id in affected_regions:
            region_score = self.score_region(region_id, grouped.get(region_id, []), global_average)
            if region_score is None:
                score_map.pop(region_id, None)
                continue
            score_map[region_id] = region_score

        return sorted(score_map.values(), key=lambda item: item.crisis_score, reverse=True)

    def score_region(
        self,
        region_id: str,
        posts: list[EnrichedPost],
        global_average_posts: float,
    ) -> RegionScore | None:
        clean_posts = [post for post in posts if not post.is_bot]
        bot_count = len(posts) - len(clean_posts)
        bot_ratio = bot_count / max(len(posts), 1)

        if not clean_posts:
            return None

        weights = settings.weights
        thresholds = settings.escalation_thresholds

        sentiment = self._sentiment_intensity(clean_posts)
        volume = self._volume_spike(clean_posts, global_average_posts * 0.6)
        geo_cluster = self._geo_cluster(clean_posts)
        trend = self._trend_acceleration(clean_posts)

        crisis_score = round(
            weights["sentiment"] * sentiment
            + weights["volume"] * volume
            + weights["geo_cluster"] * geo_cluster
            + weights["trend"] * trend,
            4,
        )
        confidence = self._confidence(clean_posts, bot_ratio)

        return RegionScore(
            region_id=region_id,
            post_count=len(clean_posts),
            bot_count=bot_count,
            bot_ratio=round(bot_ratio, 4),
            sentiment_intensity=round(sentiment, 4),
            volume_spike=round(volume, 4),
            geo_cluster=round(geo_cluster, 4),
            trend_accel=round(trend, 4),
            crisis_score=crisis_score,
            confidence=confidence,
            should_escalate=(
                crisis_score >= thresholds["crisis_score"]
                and confidence >= thresholds["confidence"]
                and len(clean_posts) >= thresholds["min_posts"]
                and bot_ratio < thresholds["max_bot_ratio"]
            ),
            avg_sentiment=round(sum(post.sentiment for post in clean_posts) / len(clean_posts), 4),
        )

    def _group_by_region(self, posts: list[EnrichedPost]) -> dict[str, list[EnrichedPost]]:
        grouped: dict[str, list[EnrichedPost]] = defaultdict(list)
        for post in posts:
            grouped[post.region_id].append(post)
        return dict(grouped)

    def _global_average(self, grouped: dict[str, list[EnrichedPost]]) -> float:
        if not grouped:
            return 0.0
        return sum(len(region_posts) for region_posts in grouped.values()) / len(grouped)

    def _sentiment_intensity(self, posts: list[EnrichedPost]) -> float:
        if not posts:
            return 0.0
        return min(sum(1 for post in posts if post.sentiment < -0.2) / len(posts), 1.0)

    def _volume_spike(self, posts: list[EnrichedPost], baseline: float) -> float:
        if baseline <= 0:
            return 0.0
        return min(len(posts) / baseline, 3.0) / 3.0

    def _geo_cluster(self, posts: list[EnrichedPost]) -> float:
        if not posts:
            return 0.0
        return min(sum(1 for post in posts if post.nlp_crisis_flag) / len(posts), 1.0)

    def _trend_acceleration(self, posts: list[EnrichedPost]) -> float:
        if len(posts) < 4:
            return 0.0
        midpoint = len(posts) // 2
        older_slice = posts[:midpoint]
        newer_slice = posts[midpoint:]
        older_rate = sum(1 for post in older_slice if post.nlp_crisis_flag) / max(len(older_slice), 1)
        newer_rate = sum(1 for post in newer_slice if post.nlp_crisis_flag) / max(len(newer_slice), 1)
        return min(max(newer_rate - older_rate + 0.5, 0.0), 1.0)

    def _confidence(self, posts: list[EnrichedPost], bot_ratio: float) -> float:
        volume_factor = min(len(posts) / 200, 1.0)
        consistency_factor = 1.0 - min(bot_ratio * 2, 1.0)
        coverage_factor = min(len(posts) / 50, 1.0)
        return round(volume_factor * consistency_factor * coverage_factor, 4)
