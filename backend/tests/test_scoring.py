from __future__ import annotations

import pytest

from app.schemas.post import EnrichedPost
from app.services.scoring_service import ScoringService


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


@pytest.fixture()
def scoring_service() -> ScoringService:
    return ScoringService()


def test_score_region_skips_all_bot_traffic(scoring_service: ScoringService):
    posts = [_make_post(is_bot=True) for _ in range(8)]
    assert scoring_service.score_region("CA-LA", posts, 10.0) is None


def test_score_region_escalates_for_strong_signal(scoring_service: ScoringService):
    posts = [_make_post(sentiment=-0.9, nlp_crisis_flag=True) for _ in range(200)]

    score = scoring_service.score_region("CA-LA", posts, 5.0)

    assert score is not None
    assert score.crisis_score > 0.5
    assert score.confidence >= 0.6
    assert score.should_escalate is True


def test_score_regions_keeps_results_sorted(scoring_service: ScoringService):
    high_signal = [
        _make_post(region_id="CA-LA", sentiment=-0.9, nlp_crisis_flag=True)
        for _ in range(30)
    ]
    low_signal = [
        _make_post(region_id="TX-HOU", sentiment=0.4, nlp_crisis_flag=False)
        for _ in range(20)
    ]

    results = scoring_service.score_regions(high_signal + low_signal)

    assert [item.crisis_score for item in results] == sorted(
        [item.crisis_score for item in results], reverse=True
    )
    assert {item.region_id for item in results} == {"CA-LA", "TX-HOU"}
