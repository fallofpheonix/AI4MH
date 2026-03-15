"""
AI4MH — Alert Models

Validated schema for alert lifecycle management.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


AlertStatus = Literal["review_required", "acknowledged", "dismissed", "resolved"]


class Alert(BaseModel):
    """An actionable alert generated when a region's crisis score exceeds the threshold."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    region: str
    score: float = Field(..., ge=0.0, le=1.0)
    status: AlertStatus = "review_required"
    confidence: float = Field(..., ge=0.0, le=1.0)
    sample_size: int = Field(..., ge=0)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    # Scoring breakdown for explainability.
    score_breakdown: Dict[str, Any] = Field(default_factory=dict)
    # Evidence post IDs linked to this alert.
    evidence_post_ids: List[str] = Field(default_factory=list)


class LogEvent(BaseModel):
    """An append-only pipeline log entry."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    event: str
    payload: Dict[str, Any] = Field(default_factory=dict)
