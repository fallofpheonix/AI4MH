"""
Crisis signal scoring engine for public-sector early warning workflows.

This module intentionally uses lightweight statistical logic only.
No heavy ML dependencies are required.
"""

from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
import math
import statistics
from typing import Any


class CrisisSignalEngine:
    """
    Compute crisis signals from social-media post batches.

    Expected post fields:
    - text
    - timestamp
    - region
    - user_id
    - sentiment_score in [-1, +1]
    """

    MIN_SAMPLE_SIZE = 50
    SPIKE_LIMIT = 3
    ALPHA = 0.3

    def __init__(
        self,
        min_sample_size: int = MIN_SAMPLE_SIZE,
        spike_limit: float = SPIKE_LIMIT,
        alpha: float = ALPHA,
        expected_regions: int = 10,
        volume_window: int = 7,
    ) -> None:
        self.min_sample_size = max(min_sample_size, 1)
        self.spike_limit = max(spike_limit, 1e-9)
        self.alpha = self._clamp(alpha)
        self.expected_regions = max(expected_regions, 1)
        self.volume_history: deque[int] = deque(maxlen=max(volume_window, 1))
        self.previous_score = 0.0
        self.audit_log: list[dict[str, Any]] = []

    @staticmethod
    def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
        return max(lo, min(hi, value))

    @staticmethod
    def _safe_mean(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def compute_sentiment_intensity(self, posts: list[dict[str, Any]]) -> float:
        """
        Compute normalized negative sentiment:
        normalized_sentiment = max(0, -mean(sentiment_scores))
        """
        scores = [float(p.get("sentiment_score", 0.0)) for p in posts]
        mean_sentiment = self._safe_mean(scores)
        return self._clamp(max(0.0, -mean_sentiment))

    def detect_volume_spike(self, posts: list[dict[str, Any]], baseline_volume: float) -> float:
        """
        Compute normalized volume spike:
        volume_spike = current_volume / baseline_volume
        volume_score = min(volume_spike / spike_limit, 1)
        """
        current_volume = len(posts)
        if baseline_volume <= 0:
            return 0.0
        volume_spike = current_volume / baseline_volume
        volume_score = volume_spike / self.spike_limit
        return self._clamp(volume_score)

    def compute_geo_cluster(self, posts: list[dict[str, Any]]) -> float:
        """
        Compute geographic clustering as dominant-region concentration:
        geo_cluster = posts_in_region / total_posts

        Since target region is not provided in method signature, this uses the
        highest-concentration region in the batch.
        """
        total_posts = len(posts)
        if total_posts == 0:
            return 0.0

        region_counts: Counter[str] = Counter(
            str(p.get("region", "unknown")) for p in posts
        )
        dominant_count = max(region_counts.values()) if region_counts else 0
        return self._clamp(dominant_count / total_posts)

    def estimate_confidence(self, posts: list[dict[str, Any]]) -> float:
        """
        Estimate confidence from:
        - sample size factor
        - geographic coverage factor
        - sentiment variance factor
        """
        sample_size = len(posts)
        if sample_size == 0:
            return 0.0

        # log(sample_size)/log(1000), clamped to [0,1]
        sample_factor = self._clamp(math.log(max(sample_size, 1)) / math.log(1000))

        regions = {str(p.get("region", "unknown")) for p in posts}
        geo_coverage = self._clamp(len(regions) / self.expected_regions)

        scores = [float(p.get("sentiment_score", 0.0)) for p in posts]
        sentiment_variance = statistics.pvariance(scores) if len(scores) > 1 else 0.0
        variance_factor = self._clamp(1.0 - sentiment_variance)

        confidence = min(sample_factor, geo_coverage, variance_factor)
        return self._clamp(confidence)

    def detect_bots(self, posts: list[dict[str, Any]]) -> set[str]:
        """
        Placeholder bot detection hook.

        Replace with frequency/content/account-age heuristics or an external
        detector when available. Returns suspected bot user_ids.
        """
        _ = posts
        return set()

    def _moving_average_baseline(self, current_volume: int) -> float:
        """
        Baseline from historical post counts. Falls back to current volume
        on cold start to avoid divide-by-zero inflation.
        """
        if self.volume_history:
            return self._safe_mean(list(self.volume_history))
        return float(current_volume)

    def _append_audit_log(
        self,
        *,
        crisis_score: float | None,
        confidence_score: float | None,
        escalation_flag: bool,
        human_review_required: bool,
        sample_size: int,
        sentiment_intensity: float | None,
        volume_score: float | None,
        geo_cluster: float | None,
        bot_count: int,
        status: str = "ok",
    ) -> None:
        """Record decision trace for governance/auditability."""
        self.audit_log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "sample_size": sample_size,
                "sentiment_intensity": sentiment_intensity,
                "volume_score": volume_score,
                "geo_cluster": geo_cluster,
                "crisis_score": crisis_score,
                "confidence_score": confidence_score,
                "escalation_flag": escalation_flag,
                "human_review_required": human_review_required,
                "bot_count": bot_count,
            }
        )

    def compute_crisis_signal(self, posts: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Main scoring entrypoint.

        Returns a structured object with:
        - crisis_score
        - confidence_score
        - escalation_flag
        - human_review_required
        plus supporting metadata for audit/debug.
        """
        sample_size = len(posts)
        suspected_bots = self.detect_bots(posts)

        if sample_size < self.min_sample_size:
            result = {
                "status": "insufficient_data",
                "crisis_score": None,
                "confidence_score": 0.0,
                "escalation_flag": False,
                "human_review_required": False,
                "sample_size": sample_size,
                "required_sample_size": self.min_sample_size,
            }
            self._append_audit_log(
                crisis_score=None,
                confidence_score=0.0,
                escalation_flag=False,
                human_review_required=False,
                sample_size=sample_size,
                sentiment_intensity=None,
                volume_score=None,
                geo_cluster=None,
                bot_count=len(suspected_bots),
                status="insufficient_data",
            )
            return result

        sentiment_intensity = self.compute_sentiment_intensity(posts)
        baseline_volume = self._moving_average_baseline(sample_size)
        volume_score = self.detect_volume_spike(posts, baseline_volume)
        geo_cluster = self.compute_geo_cluster(posts)

        raw_crisis_score = (
            0.4 * sentiment_intensity
            + 0.4 * volume_score
            + 0.2 * geo_cluster
        )
        raw_crisis_score = self._clamp(raw_crisis_score)

        smoothed_score = self.alpha * raw_crisis_score + (1.0 - self.alpha) * self.previous_score
        smoothed_score = self._clamp(smoothed_score)

        confidence_score = self.estimate_confidence(posts)

        escalation_flag = bool(smoothed_score > 0.75 and confidence_score > 0.6)
        human_review_required = escalation_flag

        result = {
            "status": "ok",
            "crisis_score": round(smoothed_score, 4),
            "confidence_score": round(confidence_score, 4),
            "escalation_flag": escalation_flag,
            "human_review_required": human_review_required,
            "signals": {
                "sentiment_intensity": round(sentiment_intensity, 4),
                "volume_score": round(volume_score, 4),
                "geo_cluster": round(geo_cluster, 4),
                "baseline_volume": round(baseline_volume, 4),
            },
            "sample_size": sample_size,
            "suspected_bot_count": len(suspected_bots),
        }

        self._append_audit_log(
            crisis_score=result["crisis_score"],
            confidence_score=result["confidence_score"],
            escalation_flag=escalation_flag,
            human_review_required=human_review_required,
            sample_size=sample_size,
            sentiment_intensity=result["signals"]["sentiment_intensity"],
            volume_score=result["signals"]["volume_score"],
            geo_cluster=result["signals"]["geo_cluster"],
            bot_count=len(suspected_bots),
        )

        # Update state for next rolling computation.
        self.previous_score = smoothed_score
        self.volume_history.append(sample_size)
        return result
