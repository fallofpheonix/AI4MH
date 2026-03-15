"""
AI4MH — Crisis Scoring Pipeline Stage

Composite weighted scoring engine across four signal dimensions:
  - sentiment_intensity
  - volume_spike
  - geo_cluster
  - trend_acceleration

All scoring formulas are preserved exactly from the original implementation.
This module has no FastAPI dependency.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from config import settings
from models.post import EnrichedPost
from models.score import RegionScore
from pipeline.aggregate import compute_global_avg, group_by_region

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ helpers


def _sentiment_intensity(posts: List[EnrichedPost]) -> float:
    """Return the fraction of posts with strongly negative sentiment (< -0.2)."""
    if not posts:
        return 0.0
    neg = sum(1 for p in posts if p.sentiment < -0.2)
    return min(neg / len(posts), 1.0)


def _volume_spike(posts: List[EnrichedPost], baseline_avg: float) -> float:
    """Return current_count / historical_baseline, scaled to [0, 1]."""
    if baseline_avg <= 0:
        return 0.0
    return min(len(posts) / baseline_avg, 3.0) / 3.0


def _geo_cluster(posts: List[EnrichedPost]) -> float:
    """Return the crisis-post fraction for the region."""
    if not posts:
        return 0.0
    crisis = sum(1 for p in posts if p.nlp_crisis_flag)
    return min(crisis / len(posts), 1.0)


def _trend_acceleration(posts: List[EnrichedPost]) -> float:
    """
    Simplified trend: ratio of crisis posts in the newest half vs oldest half.

    Returns a value in [0, 1] where > 0.5 indicates acceleration.
    Replace with an OLS slope on a real time-series for production use.
    """
    if len(posts) < 4:
        return 0.0
    mid = len(posts) // 2
    old_crisis = sum(1 for p in posts[:mid] if p.nlp_crisis_flag)
    new_crisis = sum(1 for p in posts[mid:] if p.nlp_crisis_flag)
    old_rate = old_crisis / max(mid, 1)
    new_rate = new_crisis / max(len(posts) - mid, 1)
    return min(max(new_rate - old_rate + 0.5, 0), 1.0)


def _confidence(posts: List[EnrichedPost], bot_ratio: float) -> float:
    """Estimate confidence from volume, consistency, and coverage signals."""
    volume_factor = min(len(posts) / 200, 1.0)
    consistency_factor = 1.0 - min(bot_ratio * 2, 1.0)
    coverage_factor = min(len(posts) / 50, 1.0)
    return round(volume_factor * consistency_factor * coverage_factor, 4)


# ------------------------------------------------------------------ public API


def score_region(
    region_id: str,
    posts: List[EnrichedPost],
    global_avg_posts: float,
) -> Optional[RegionScore]:
    """
    Compute the full crisis score for one region.

    Parameters
    ----------
    region_id:
        Identifier of the region being scored.
    posts:
        All NLP-enriched posts for this region.
    global_avg_posts:
        Mean post count per region across all active regions.

    Returns ``None`` when all posts are from bots (no clean signal).
    """
    clean = [p for p in posts if not p.is_bot]
    bots = [p for p in posts if p.is_bot]
    bot_ratio = len(bots) / max(len(posts), 1)

    if not clean:
        logger.debug("Region %s: all posts are bots — skipping.", region_id)
        return None

    w = settings.weights
    et = settings.escalation_thresholds

    s_intensity = _sentiment_intensity(clean)
    v_spike = _volume_spike(clean, global_avg_posts * 0.6)
    g_cluster = _geo_cluster(clean)
    t_accel = _trend_acceleration(clean)

    score = round(
        w["sentiment"] * s_intensity
        + w["volume"] * v_spike
        + w["geo_cluster"] * g_cluster
        + w["trend"] * t_accel,
        4,
    )

    conf = _confidence(clean, bot_ratio)

    should_escalate = (
        score >= et["crisis_score"]
        and conf >= et["confidence"]
        and len(clean) >= et["min_posts"]
        and bot_ratio < et["max_bot_ratio"]
    )

    return RegionScore(
        region_id=region_id,
        post_count=len(clean),
        bot_count=len(bots),
        bot_ratio=round(bot_ratio, 4),
        sentiment_intensity=round(s_intensity, 4),
        volume_spike=round(v_spike, 4),
        geo_cluster=round(g_cluster, 4),
        trend_accel=round(t_accel, 4),
        crisis_score=score,
        confidence=conf,
        should_escalate=should_escalate,
        avg_sentiment=round(
            sum(p.sentiment for p in clean) / len(clean), 4
        ),
    )


def score_all_regions(
    enriched_posts: List[EnrichedPost],
    affected_regions: Optional[Set[str]] = None,
    existing_scores: Optional[List[RegionScore]] = None,
) -> List[RegionScore]:
    """
    Compute crisis scores for all (or only *affected*) regions.

    Parameters
    ----------
    enriched_posts:
        Full current post pool.
    affected_regions:
        When provided, only recompute scores for these region IDs and merge
        the results with *existing_scores* for unaffected regions.
        Pass ``None`` to recompute all regions.
    existing_scores:
        The previous score snapshot, used when *affected_regions* is given.

    Returns a list sorted by crisis_score descending.
    """
    groups = group_by_region(enriched_posts)
    global_avg = compute_global_avg(groups)

    if affected_regions is not None and existing_scores is not None:
        # Only recompute scores for affected regions; reuse the rest.
        score_map = {s.region_id: s for s in existing_scores}
        for region_id in affected_regions:
            posts = groups.get(region_id, [])
            result = score_region(region_id, posts, global_avg)
            if result:
                score_map[region_id] = result
            else:
                score_map.pop(region_id, None)
        results = list(score_map.values())
    else:
        results = []
        for region_id, posts in groups.items():
            result = score_region(region_id, posts, global_avg)
            if result:
                results.append(result)

    return sorted(results, key=lambda r: r.crisis_score, reverse=True)
