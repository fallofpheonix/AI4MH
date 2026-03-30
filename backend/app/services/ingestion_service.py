from __future__ import annotations

import datetime as dt
import random

from app.schemas.post import RawPost

REGIONS: list[dict[str, int | str]] = [
    {"id": "CA-LA", "name": "Los Angeles, CA", "population": 3_980_000},
    {"id": "TX-HOU", "name": "Houston, TX", "population": 2_300_000},
    {"id": "NY-NYC", "name": "New York, NY", "population": 8_340_000},
    {"id": "IL-CHI", "name": "Chicago, IL", "population": 2_700_000},
    {"id": "AZ-PHX", "name": "Phoenix, AZ", "population": 1_680_000},
    {"id": "PA-PHI", "name": "Philadelphia, PA", "population": 1_580_000},
    {"id": "WV-CHA", "name": "Charleston, WV", "population": 46_000},
    {"id": "KY-HAZ", "name": "Hazard, KY", "population": 4_700},
    {"id": "OH-CHI", "name": "Chillicothe, OH", "population": 21_000},
]

CRISIS_TEXTS = [
    "I can't go on anymore",
    "thinking about suicide, no way out",
    "life feels completely hopeless",
    "overdose seems easier than this",
    "nobody would miss me if I was gone",
    "I've been cutting again, can't stop",
    "relapsed after 2 years, feel so hopeless",
    "can't take it anymore, done with everything",
]

NORMAL_TEXTS = [
    "today was a good day overall",
    "going for a walk to clear my head",
    "feeling okay, therapy is helping",
    "started a new medication, cautiously hopeful",
    "support group really helped tonight",
    "had my first good day in months",
]

SUBREDDITS = ["depression", "mentalhealth", "SuicideWatch", "addiction", "anxiety"]


class IngestionService:
    def __init__(self) -> None:
        self._regions_by_id = {str(item["id"]): item for item in REGIONS}

    @property
    def regions(self) -> list[dict[str, int | str]]:
        return REGIONS

    def get_population(self, region_id: str) -> int | None:
        region = self._regions_by_id.get(region_id)
        if region is None:
            return None
        return int(region["population"])

    def build_dataset(self, size: int = 300) -> list[RawPost]:
        if size <= 0:
            return []
        return [self._build_post(is_bot=random.random() < 0.07) for _ in range(size)]

    def _build_post(self, *, is_bot: bool) -> RawPost:
        is_crisis = random.random() < 0.25
        region = random.choice(REGIONS)
        text_pool = CRISIS_TEXTS if is_crisis else NORMAL_TEXTS
        return RawPost(
            id=f"post_{random.randint(100_000, 999_999)}",
            text=random.choice(text_pool),
            subreddit=random.choice(SUBREDDITS),
            region_id=str(region["id"]),
            region_name=str(region["name"]),
            timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
            upvotes=random.randint(0, 500),
            comments=random.randint(0, 80),
            is_bot=is_bot,
            is_crisis_text=is_crisis,
            ground_truth_crisis=is_crisis,
        )
