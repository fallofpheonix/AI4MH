"""
AI4MH — Governance & Risk Filters
Bot detection, media spike dampening, population normalization.
"""

from ingest_posts import REGIONS

# ── Bot Detection ─────────────────────────────────────────────────────────────

BOT_POST_RATE_THRESHOLD = 20   # posts per hour
BOT_DUPLICATE_THRESHOLD = 0.8  # 80% identical content = bot cluster

def is_bot_by_rate(posts_last_hour: int) -> bool:
    return posts_last_hour > BOT_POST_RATE_THRESHOLD

def bot_ratio_for_region(posts: list[dict]) -> float:
    total = len(posts)
    if total == 0:
        return 0.0
    bots = sum(1 for p in posts if p.get("is_bot", False))
    return round(bots / total, 4)

def filter_bots(posts: list[dict]) -> tuple[list[dict], list[dict]]:
    """Returns (clean_posts, removed_bots)."""
    clean = [p for p in posts if not p.get("is_bot", False)]
    bots  = [p for p in posts if p.get("is_bot", False)]
    return clean, bots


# ── Media Spike Detection ─────────────────────────────────────────────────────

# In production: check NLP overlap with Reuters/AP headline feed
KNOWN_MEDIA_EVENTS = [
    "celebrity_suicide", "national_overdose_report", "mass_shooting",
]

def is_media_driven_spike(dominant_topic: str) -> bool:
    return dominant_topic in KNOWN_MEDIA_EVENTS

def apply_media_dampening(score: float, is_media_event: bool) -> float:
    """Reduce score weight if spike is driven by national news."""
    if is_media_event:
        return round(score * 0.6, 4)
    return score


# ── Population Normalization ──────────────────────────────────────────────────

_POP_MAP = {r["id"]: r["population"] for r in REGIONS}

def population_tier(region_id: str) -> str:
    pop = _POP_MAP.get(region_id, 500000)
    if pop < 100_000:
        return "rural"
    elif pop < 1_000_000:
        return "suburban"
    return "urban"

def normalize_by_population(raw_score: float, region_id: str) -> float:
    """
    Rural regions get a boost since low post volume underrepresents true signal.
    Urban regions are lightly penalized for sheer volume dominance.
    """
    tier = population_tier(region_id)
    multiplier = {"rural": 1.30, "suburban": 1.05, "urban": 1.00}[tier]
    return round(min(raw_score * multiplier, 1.0), 4)

def min_posts_threshold(region_id: str) -> int:
    """Rural areas need fewer posts to be considered valid."""
    tier = population_tier(region_id)
    return {"rural": 5, "suburban": 15, "urban": 25}[tier]


# ── Apply All Filters ─────────────────────────────────────────────────────────

def apply_governance(score_result: dict, media_topic: str = "") -> dict:
    """
    Wraps a raw score_region() result with governance adjustments.
    """
    region_id  = score_result["region_id"]
    raw_score  = score_result["crisis_score"]

    # 1. Population normalization
    norm_score = normalize_by_population(raw_score, region_id)

    # 2. Media dampening
    is_media   = is_media_driven_spike(media_topic)
    final_score= apply_media_dampening(norm_score, is_media)

    # 3. Tier-aware minimum posts check
    min_posts  = min_posts_threshold(region_id)
    meets_min  = score_result["post_count"] >= min_posts

    return {
        **score_result,
        "population_tier":     population_tier(region_id),
        "normalized_score":    norm_score,
        "media_event_detected":is_media,
        "final_score":         final_score,
        "meets_min_posts":     meets_min,
        "governance_ok":       meets_min and score_result["bot_ratio"] < 0.25,
    }
