"""
AI4MH — NLP Enrichment Pipeline Stage

Applies VADER sentiment analysis and crisis keyword detection to raw posts.
This module has no FastAPI dependency and operates purely on domain models.
"""

from __future__ import annotations

import logging
from typing import List

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import settings
from models.post import EnrichedPost, RawPost

logger = logging.getLogger(__name__)

_analyzer = SentimentIntensityAnalyzer()


def sentiment_score(text: str) -> float:
    """Return the VADER compound score in [-1, 1]. Negative indicates distress."""
    return _analyzer.polarity_scores(text)["compound"]


def keyword_score(text: str) -> dict:
    """Return a dict with ``count`` and ``terms`` listing matched crisis keywords."""
    lower = text.lower()
    matched = [t for t in settings.crisis_terms if t in lower]
    return {"count": len(matched), "terms": matched}


def enrich_post(post: RawPost) -> EnrichedPost:
    """
    Enrich a single raw post with NLP signals.

    Adds ``sentiment``, ``keyword_count``, ``keyword_terms``,
    ``nlp_crisis_flag``, and ``ai_correct``.
    """
    try:
        sentiment = round(sentiment_score(post.text), 4)
        kw = keyword_score(post.text)
        predicted_crisis = sentiment < -0.4 or kw["count"] > 0
        ground_truth = post.ground_truth_crisis
        return EnrichedPost(
            **post.model_dump(),
            sentiment=sentiment,
            keyword_count=kw["count"],
            keyword_terms=kw["terms"],
            nlp_crisis_flag=predicted_crisis,
            ai_correct=predicted_crisis == ground_truth,
        )
    except Exception:
        logger.exception("NLP enrichment failed for post %s", post.id)
        raise


def enrich_batch(posts: List[RawPost]) -> List[EnrichedPost]:
    """Enrich a list of raw posts; skip and log any that fail."""
    results: List[EnrichedPost] = []
    for post in posts:
        try:
            results.append(enrich_post(post))
        except Exception:
            logger.warning("Skipping post %s due to enrichment error.", post.id)
    return results
