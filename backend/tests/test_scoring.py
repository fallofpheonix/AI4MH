"""
Unit tests for the crisis scoring pipeline stage.

Tests cover all four signal functions, confidence estimation, region scoring,
and the full score_all_regions aggregation.
"""

from __future__ import annotations

import sys
import os

# Ensure backend root is on the path.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from models.post import EnrichedPost
from pipeline.score import (
    _confidence,
    _geo_cluster,
    _sentiment_intensity,
    _trend_acceleration,
    _volume_spike,
    score_all_regions,
    score_region,
)


# ------------------------------------------------------------------ fixtures


def _make_post(
    region_id: str = "CA-LA",
    sentiment: float = 0.0,
    nlp_crisis_flag: bool = False,
    is_bot: bool = False,
) -> EnrichedPost:
    return EnrichedPost(
        id="post_1",
        text="test text",
        subreddit="mentalhealth",
        region_id=region_id,
        region_name="Test Region",
        timestamp="2024-01-01T00:00:00+00:00",
        upvotes=0,
        comments=0,
        is_bot=is_bot,
        is_crisis_text=nlp_crisis_flag,
        ground_truth_crisis=nlp_crisis_flag,
        sentiment=sentiment,
        keyword_count=0,
        keyword_terms=[],
        nlp_crisis_flag=nlp_crisis_flag,
        ai_correct=True,
    )


# ------------------------------------------------------------------ sentiment_intensity


class TestSentimentIntensity:
    def test_empty_returns_zero(self):
        assert _sentiment_intensity([]) == 0.0

    def test_all_positive_returns_zero(self):
        posts = [_make_post(sentiment=0.5) for _ in range(10)]
        assert _sentiment_intensity(posts) == 0.0

    def test_all_strongly_negative_returns_one(self):
        posts = [_make_post(sentiment=-0.5) for _ in range(10)]
        assert _sentiment_intensity(posts) == 1.0

    def test_half_negative(self):
        posts = [_make_post(sentiment=-0.5)] * 5 + [_make_post(sentiment=0.5)] * 5
        assert _sentiment_intensity(posts) == pytest.approx(0.5)

    def test_threshold_boundary(self):
        # Exactly -0.2 is NOT strongly negative (< -0.2 is the condition).
        posts = [_make_post(sentiment=-0.2)]
        assert _sentiment_intensity(posts) == 0.0
        posts = [_make_post(sentiment=-0.21)]
        assert _sentiment_intensity(posts) == 1.0


# ------------------------------------------------------------------ volume_spike


class TestVolumeSpike:
    def test_zero_baseline_returns_zero(self):
        posts = [_make_post() for _ in range(10)]
        assert _volume_spike(posts, 0.0) == 0.0

    def test_at_baseline_returns_one_third(self):
        # 10 posts with baseline_avg=10.0: 10/10 = 1.0 → min(1.0, 3.0)/3.0 = 1/3.
        posts = [_make_post() for _ in range(10)]
        result = _volume_spike(posts, 10.0)
        assert result == pytest.approx(1.0 / 3.0, abs=1e-4)

    def test_capped_at_one(self):
        posts = [_make_post() for _ in range(300)]
        result = _volume_spike(posts, 1.0)
        assert result == pytest.approx(1.0)

    def test_empty_posts(self):
        assert _volume_spike([], 10.0) == 0.0


# ------------------------------------------------------------------ geo_cluster


class TestGeoCluster:
    def test_empty_returns_zero(self):
        assert _geo_cluster([]) == 0.0

    def test_no_crisis_posts(self):
        posts = [_make_post(nlp_crisis_flag=False) for _ in range(10)]
        assert _geo_cluster(posts) == 0.0

    def test_all_crisis_posts(self):
        posts = [_make_post(nlp_crisis_flag=True) for _ in range(10)]
        assert _geo_cluster(posts) == 1.0

    def test_half_crisis(self):
        posts = [_make_post(nlp_crisis_flag=True)] * 5 + [
            _make_post(nlp_crisis_flag=False)
        ] * 5
        assert _geo_cluster(posts) == pytest.approx(0.5)


# ------------------------------------------------------------------ trend_acceleration


class TestTrendAcceleration:
    def test_too_few_posts_returns_zero(self):
        posts = [_make_post() for _ in range(3)]
        assert _trend_acceleration(posts) == 0.0

    def test_uniform_crisis_returns_half(self):
        # Same rate in both halves → new_rate - old_rate = 0 → result = 0.5.
        posts = [_make_post(nlp_crisis_flag=True) for _ in range(10)]
        assert _trend_acceleration(posts) == pytest.approx(0.5)

    def test_accelerating_trend(self):
        old_half = [_make_post(nlp_crisis_flag=False)] * 5
        new_half = [_make_post(nlp_crisis_flag=True)] * 5
        result = _trend_acceleration(old_half + new_half)
        assert result > 0.5

    def test_decelerating_trend(self):
        old_half = [_make_post(nlp_crisis_flag=True)] * 5
        new_half = [_make_post(nlp_crisis_flag=False)] * 5
        result = _trend_acceleration(old_half + new_half)
        assert result < 0.5

    def test_clamped_to_zero_one(self):
        old_half = [_make_post(nlp_crisis_flag=True)] * 50
        new_half = [_make_post(nlp_crisis_flag=False)] * 50
        result = _trend_acceleration(old_half + new_half)
        assert 0.0 <= result <= 1.0


# ------------------------------------------------------------------ confidence


class TestConfidence:
    def test_zero_posts_zero_confidence(self):
        posts: list[EnrichedPost] = []
        assert _confidence(posts, 0.0) == 0.0

    def test_high_bot_ratio_reduces_confidence(self):
        posts = [_make_post() for _ in range(200)]
        low = _confidence(posts, 0.0)
        high = _confidence(posts, 0.5)
        assert low > high

    def test_more_posts_increases_confidence(self):
        few = [_make_post() for _ in range(10)]
        many = [_make_post() for _ in range(200)]
        assert _confidence(few, 0.0) < _confidence(many, 0.0)

    def test_max_confidence(self):
        posts = [_make_post() for _ in range(200)]
        assert _confidence(posts, 0.0) == pytest.approx(1.0)


# ------------------------------------------------------------------ score_region


class TestScoreRegion:
    def test_all_bots_returns_none(self):
        posts = [_make_post(is_bot=True) for _ in range(10)]
        result = score_region("CA-LA", posts, 10.0)
        assert result is None

    def test_valid_region_returns_score(self):
        posts = [_make_post(sentiment=-0.5, nlp_crisis_flag=True) for _ in range(20)]
        result = score_region("CA-LA", posts, 10.0)
        assert result is not None
        assert result.region_id == "CA-LA"
        assert 0.0 <= result.crisis_score <= 1.0
        assert 0.0 <= result.confidence <= 1.0

    def test_score_fields_present(self):
        posts = [_make_post() for _ in range(15)]
        result = score_region("TX-HOU", posts, 10.0)
        assert result is not None
        assert hasattr(result, "sentiment_intensity")
        assert hasattr(result, "volume_spike")
        assert hasattr(result, "geo_cluster")
        assert hasattr(result, "trend_accel")
        assert hasattr(result, "should_escalate")

    def test_high_crisis_signal_high_score(self):
        posts = [
            _make_post(sentiment=-0.9, nlp_crisis_flag=True) for _ in range(30)
        ]
        result = score_region("NY-NYC", posts, 5.0)
        assert result is not None
        assert result.crisis_score > 0.5


# ------------------------------------------------------------------ score_all_regions


class TestScoreAllRegions:
    def test_empty_posts_returns_empty(self):
        assert score_all_regions([]) == []

    def test_sorted_descending(self):
        # Mix of regions with different crisis signals.
        high = [
            _make_post(region_id="CA-LA", sentiment=-0.9, nlp_crisis_flag=True)
            for _ in range(30)
        ]
        low = [
            _make_post(region_id="TX-HOU", sentiment=0.5, nlp_crisis_flag=False)
            for _ in range(30)
        ]
        results = score_all_regions(high + low)
        scores = [r.crisis_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_affected_regions_partial_update(self):
        posts = [
            _make_post(region_id="CA-LA", sentiment=-0.5, nlp_crisis_flag=True)
            for _ in range(20)
        ] + [
            _make_post(region_id="TX-HOU", sentiment=0.5, nlp_crisis_flag=False)
            for _ in range(20)
        ]
        full_scores = score_all_regions(posts)

        # Partial update: only CA-LA affected.
        partial = score_all_regions(
            posts,
            affected_regions={"CA-LA"},
            existing_scores=full_scores,
        )
        region_ids = {r.region_id for r in partial}
        assert "CA-LA" in region_ids
        assert "TX-HOU" in region_ids
