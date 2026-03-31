from __future__ import annotations

import datetime as dt
import random

from app.fixtures.synthetic_posts import CRISIS_TEXTS, NORMAL_TEXTS, REGIONS, SUBREDDITS
from app.schemas.post import RawPost


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
