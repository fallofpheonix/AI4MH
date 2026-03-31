from __future__ import annotations

from app.schemas.alert import Alert
from app.schemas.post import EnrichedPost
from app.schemas.score import RegionScore
from app.services.alert_service import AlertService
from tests.fakes.memory_store import MemoryStore


def _score(
    *,
    region_id: str = "CA-LA",
    crisis_score: float = 0.9,
    confidence: float = 0.8,
    should_escalate: bool = True,
) -> RegionScore:
    return RegionScore(
        region_id=region_id,
        post_count=25,
        bot_count=1,
        bot_ratio=0.04,
        sentiment_intensity=0.8,
        volume_spike=0.7,
        geo_cluster=0.9,
        trend_accel=0.6,
        crisis_score=crisis_score,
        confidence=confidence,
        should_escalate=should_escalate,
        avg_sentiment=-0.5,
    )


def _post(*, region_id: str = "CA-LA", post_id: str = "post_1") -> EnrichedPost:
    return EnrichedPost(
        id=post_id,
        text="test text",
        subreddit="mentalhealth",
        region_id=region_id,
        region_name="Test Region",
        timestamp="2024-01-01T00:00:00+00:00",
        upvotes=0,
        comments=0,
        is_bot=False,
        is_crisis_text=True,
        ground_truth_crisis=True,
        sentiment=-0.8,
        keyword_count=1,
        keyword_terms=["crisis"],
        nlp_crisis_flag=True,
        ai_correct=True,
    )


def test_rebuild_alerts_requires_should_escalate():
    store = MemoryStore()
    service = AlertService(store)

    logs = service.rebuild_alerts(
        [_score(should_escalate=False, crisis_score=0.99)],
        {"CA-LA": [_post()]},
    )

    assert logs == []
    assert store.get_alerts() == []


def test_rebuild_alerts_reuses_existing_review_required_alert():
    store = MemoryStore()
    existing = Alert(id="existing-alert", region="CA-LA", score=0.76, confidence=0.65, sample_size=20)
    store.save_alerts([existing])
    service = AlertService(store)

    logs = service.rebuild_alerts([_score(crisis_score=0.91)], {"CA-LA": [_post(post_id="post_2")]})

    alerts = store.get_alerts()
    assert logs == []
    assert len(alerts) == 1
    assert alerts[0].id == "existing-alert"
    assert alerts[0].score == 0.91
    assert alerts[0].evidence_post_ids == ["post_2"]


def test_rebuild_alerts_preserves_acknowledged_alert_when_signal_cools():
    store = MemoryStore()
    existing = Alert(
        id="ack-alert",
        region="CA-LA",
        score=0.88,
        status="acknowledged",
        confidence=0.8,
        sample_size=22,
    )
    store.save_alerts([existing])
    service = AlertService(store)

    logs = service.rebuild_alerts(
        [_score(should_escalate=False, crisis_score=0.4)],
        {"CA-LA": [_post()]},
    )

    alerts = store.get_alerts()
    assert logs == []
    assert len(alerts) == 1
    assert alerts[0].id == "ack-alert"
    assert alerts[0].status == "acknowledged"
