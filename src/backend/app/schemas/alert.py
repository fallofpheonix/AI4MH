from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


AlertStatus = Literal["review_required", "acknowledged", "dismissed", "resolved"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    region: str
    score: float = Field(..., ge=0.0, le=1.0)
    status: AlertStatus = "review_required"
    confidence: float = Field(..., ge=0.0, le=1.0)
    sample_size: int = Field(..., ge=0)
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    evidence_post_ids: list[str] = Field(default_factory=list)


class LogEvent(BaseModel):
    timestamp: str = Field(default_factory=utc_now_iso)
    event: str
    payload: dict[str, Any] = Field(default_factory=dict)
