"""
AI4MH — Region Score Models

Validated schema for crisis score snapshots per region.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RegionScore(BaseModel):
    """Crisis-score snapshot for a single geographic region."""

    region_id: str
    post_count: int = Field(..., ge=0)
    bot_count: int = Field(..., ge=0)
    bot_ratio: float = Field(..., ge=0.0, le=1.0)
    sentiment_intensity: float = Field(..., ge=0.0, le=1.0)
    volume_spike: float = Field(..., ge=0.0, le=1.0)
    geo_cluster: float = Field(..., ge=0.0, le=1.0)
    trend_accel: float = Field(..., ge=0.0, le=1.0)
    crisis_score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    should_escalate: bool
    avg_sentiment: float
