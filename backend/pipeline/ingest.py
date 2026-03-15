"""
AI4MH — Ingestion Pipeline Stage

Generates or replays synthetic Reddit-style posts across US regions.
Swap ``generate_post()`` with a real PRAW call for production use.
"""

from __future__ import annotations

import datetime
import random

from models.post import RawPost

REGIONS: list[dict] = [
    {"id": "CA-LA",  "name": "Los Angeles, CA",  "population": 3980000},
    {"id": "TX-HOU", "name": "Houston, TX",       "population": 2300000},
    {"id": "NY-NYC", "name": "New York, NY",      "population": 8340000},
    {"id": "IL-CHI", "name": "Chicago, IL",       "population": 2700000},
    {"id": "AZ-PHX", "name": "Phoenix, AZ",       "population": 1680000},
    {"id": "PA-PHI", "name": "Philadelphia, PA",  "population": 1580000},
    {"id": "WV-CHA", "name": "Charleston, WV",    "population": 46000},
    {"id": "KY-HAZ", "name": "Hazard, KY",        "population": 4700},
    {"id": "OH-CHI", "name": "Chillicothe, OH",   "population": 21000},
]

_CRISIS_TEXTS: list[str] = [
    "I can't go on anymore",
    "thinking about suicide, no way out",
    "life feels completely hopeless",
    "overdose seems easier than this",
    "nobody would miss me if I was gone",
    "I've been cutting again, can't stop",
    "relapsed after 2 years, feel so hopeless",
    "can't take it anymore, done with everything",
]

_NORMAL_TEXTS: list[str] = [
    "today was a good day overall",
    "going for a walk to clear my head",
    "feeling okay, therapy is helping",
    "started a new medication, cautiously hopeful",
    "support group really helped tonight",
    "had my first good day in months",
]

_SUBREDDITS: list[str] = [
    "depression",
    "mentalhealth",
    "SuicideWatch",
    "addiction",
    "anxiety",
]


def generate_post(is_bot: bool = False) -> RawPost:
    """Return a single synthetic post as a validated :class:`RawPost`."""
    is_crisis = random.random() < 0.25
    text = random.choice(_CRISIS_TEXTS if is_crisis else _NORMAL_TEXTS)
    region = random.choice(REGIONS)
    return RawPost(
        id=f"post_{random.randint(100_000, 999_999)}",
        text=text,
        subreddit=random.choice(_SUBREDDITS),
        region_id=region["id"],
        region_name=region["name"],
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        upvotes=random.randint(0, 500),
        comments=random.randint(0, 80),
        is_bot=is_bot,
        is_crisis_text=is_crisis,
        ground_truth_crisis=is_crisis,
    )


def generate_dataset(n: int = 300) -> list[RawPost]:
    """Return *n* synthetic posts with a ~7 % bot rate."""
    return [generate_post(is_bot=random.random() < 0.07) for _ in range(n)]
