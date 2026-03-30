from __future__ import annotations

from pydantic import BaseModel, Field


class RawPost(BaseModel):
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
    sentiment: float = Field(..., ge=-1.0, le=1.0)
    keyword_count: int = Field(default=0, ge=0)
    keyword_terms: list[str] = Field(default_factory=list)
    nlp_crisis_flag: bool
    ai_correct: bool
