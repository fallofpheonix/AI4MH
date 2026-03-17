from __future__ import annotations

import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.config import settings
from app.core.models.post import EnrichedPost, RawPost

logger = logging.getLogger(__name__)


class EnrichmentService:
    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def enrich_batch(self, posts: list[RawPost]) -> list[EnrichedPost]:
        enriched: list[EnrichedPost] = []
        for post in posts:
            try:
                enriched.append(self.enrich_post(post))
            except Exception:
                logger.warning("dropping post after enrichment failure", extra={"post_id": post.id})
        return enriched

    def enrich_post(self, post: RawPost) -> EnrichedPost:
        sentiment = round(self._score_sentiment(post.text), 4)
        keyword_terms = self._match_terms(post.text)
        inferred_crisis = sentiment < -0.4 or bool(keyword_terms)
        return EnrichedPost(
            **post.model_dump(),
            sentiment=sentiment,
            keyword_count=len(keyword_terms),
            keyword_terms=keyword_terms,
            nlp_crisis_flag=inferred_crisis,
            ai_correct=inferred_crisis == post.ground_truth_crisis,
        )

    def _score_sentiment(self, text: str) -> float:
        if not text.strip():
            return 0.0
        return self._analyzer.polarity_scores(text)["compound"]

    def _match_terms(self, text: str) -> list[str]:
        lowered = text.lower()
        return [term for term in settings.crisis_terms if term in lowered]
