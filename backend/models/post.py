"""
AI4MH — Post Models

Validated schema for raw and NLP-enriched posts.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RawPost(BaseModel):
    """A post as received from the ingestion layer before NLP processing."""

    id: str
    text: str
    subreddit: str
    region_id: str
    region_name: str
    timestamp: str
    upvotes: int = 0
    comments: int = 0
    is_bot: bool = False
    is_crisis_text: bool = False
    ground_truth_crisis: bool = False


class EnrichedPost(RawPost):
    """A post after NLP enrichment has been applied."""

    sentiment: float = Field(
        ..., ge=-1.0, le=1.0, description="VADER compound sentiment score."
    )
    keyword_count: int = Field(..., ge=0)
    keyword_terms: List[str] = Field(default_factory=list)
    nlp_crisis_flag: bool
    ai_correct: bool
