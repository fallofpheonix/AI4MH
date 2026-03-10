"""
AI4MH — Crisis Scoring Engine
Composite weighted formula across 4 signal dimensions.
"""

import math
from collections import defaultdict

# Signal weights (must sum to 1.0)
WEIGHTS = {
    "sentiment":  0.35,
    "volume":     0.30,
    "geo_cluster":0.20,
    "trend":      0.15,
}

ESCALATION_THRESHOLDS = {
    "crisis_score": 0.70,
    "confidence":   0.60,
    "min_posts":    10,
    "max_bot_ratio":0.25,
}


def _sentiment_intensity(posts: list[dict]) -> float:
    """Fraction of posts with strongly negative sentiment."""
    if not posts:
        return 0.0
    neg = sum(1 for p in posts if p.get("sentiment", 0) < -0.2)
    return min(neg / len(posts), 1.0)


def _volume_spike(posts: list[dict], baseline_avg: float) -> float:
    """current_count / historical_baseline, capped at 1."""
    if baseline_avg <= 0:
        return 0.0
    return min(len(posts) / baseline_avg, 3.0) / 3.0


def _geo_cluster(posts: list[dict]) -> float:
    """Crisis posts / total posts in region."""
    if not posts:
        return 0.0
    crisis = sum(1 for p in posts if p.get("nlp_crisis_flag", False))
    return min(crisis / len(posts), 1.0)


def _trend_acceleration(posts: list[dict]) -> float:
    """
    Simplified: ratio of crisis posts in newest half vs oldest half.
    Positive = accelerating. Replace with OLS slope on real time-series.
    """
    if len(posts) < 4:
        return 0.0
    mid = len(posts) // 2
    old_crisis = sum(1 for p in posts[:mid]  if p.get("nlp_crisis_flag"))
    new_crisis = sum(1 for p in posts[mid:]  if p.get("nlp_crisis_flag"))
    old_rate = old_crisis / max(mid, 1)
    new_rate = new_crisis / max(len(posts) - mid, 1)
    return min(max(new_rate - old_rate + 0.5, 0), 1.0)


def _confidence(posts: list[dict], bot_ratio: float) -> float:
    volume_factor      = min(len(posts) / 200, 1.0)
    consistency_factor = 1.0 - min(bot_ratio * 2, 1.0)
    coverage_factor    = min(len(posts) / 50, 1.0)
    return round(volume_factor * consistency_factor * coverage_factor, 4)


def score_region(region_id: str, posts: list[dict], global_avg_posts: float) -> dict:
    """
    Compute full crisis score for one region.
    posts: NLP-enriched post dicts for this region only.
    """
    clean   = [p for p in posts if not p.get("is_bot")]
    bots    = [p for p in posts if p.get("is_bot")]
    bot_ratio = len(bots) / max(len(posts), 1)

    if not clean:
        return None

    s_intensity = _sentiment_intensity(clean)
    v_spike     = _volume_spike(clean, global_avg_posts * 0.6)
    g_cluster   = _geo_cluster(clean)
    t_accel     = _trend_acceleration(clean)

    score = round(
        WEIGHTS["sentiment"]   * s_intensity +
        WEIGHTS["volume"]      * v_spike     +
        WEIGHTS["geo_cluster"] * g_cluster   +
        WEIGHTS["trend"]       * t_accel,
        4
    )

    conf = _confidence(clean, bot_ratio)

    should_escalate = (
        score     >= ESCALATION_THRESHOLDS["crisis_score"] and
        conf      >= ESCALATION_THRESHOLDS["confidence"]   and
        len(clean)>= ESCALATION_THRESHOLDS["min_posts"]    and
        bot_ratio <  ESCALATION_THRESHOLDS["max_bot_ratio"]
    )

    return {
        "region_id":          region_id,
        "post_count":         len(clean),
        "bot_count":          len(bots),
        "bot_ratio":          round(bot_ratio, 4),
        "sentiment_intensity":round(s_intensity, 4),
        "volume_spike":       round(v_spike, 4),
        "geo_cluster":        round(g_cluster, 4),
        "trend_accel":        round(t_accel, 4),
        "crisis_score":       score,
        "confidence":         conf,
        "should_escalate":    should_escalate,
        "avg_sentiment":      round(
            sum(p.get("sentiment",0) for p in clean) / len(clean), 4
        ),
    }


def score_all_regions(enriched_posts: list[dict]) -> list[dict]:
    by_region = defaultdict(list)
    for p in enriched_posts:
        by_region[p["region_id"]].append(p)

    global_avg = sum(len(v) for v in by_region.values()) / max(len(by_region), 1)

    results = []
    for region_id, posts in by_region.items():
        result = score_region(region_id, posts, global_avg)
        if result:
            results.append(result)

    return sorted(results, key=lambda r: r["crisis_score"], reverse=True)
