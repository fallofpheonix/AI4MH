"""
AI4MH — Configuration Module

All runtime-tunable constants are defined here using Pydantic Settings.
Values can be overridden through environment variables with the ``AI4MH_``
prefix (e.g. ``AI4MH_ALERT_THRESHOLD=0.80``).
"""

from __future__ import annotations

import json
import pathlib
from typing import Dict

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_LEXICON_PATH = pathlib.Path(__file__).parent / "lexicons" / "crisis_terms_v1.json"


def _default_crisis_terms() -> list[str]:
    """Load crisis terms from the bundled lexicon file."""
    with open(_LEXICON_PATH, encoding="utf-8") as fh:
        return json.load(fh)


class Settings(BaseSettings):
    """Application-wide configuration validated at startup."""

    model_config = SettingsConfigDict(env_prefix="AI4MH_", env_file=".env")

    # ---------- alert thresholds ----------
    alert_threshold: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Minimum crisis_score required to create a review alert.",
    )

    # ---------- storage ----------
    max_posts: int = Field(
        default=500,
        ge=1,
        description="Maximum number of enriched posts retained in memory.",
    )

    # ---------- scoring weights (must sum to 1.0) ----------
    weights: Dict[str, float] = Field(
        default={
            "sentiment": 0.35,
            "volume": 0.30,
            "geo_cluster": 0.20,
            "trend": 0.15,
        },
        description="Per-signal weights for the composite crisis score.",
    )

    # ---------- escalation gate ----------
    escalation_thresholds: Dict[str, float] = Field(
        default={
            "crisis_score": 0.70,
            "confidence": 0.60,
            "min_posts": 10,
            "max_bot_ratio": 0.25,
        },
        description="Minimum values required before escalation is flagged.",
    )

    # ---------- lexicon ----------
    crisis_terms: list[str] = Field(
        default_factory=_default_crisis_terms,
        description="Crisis keyword list loaded from lexicons/crisis_terms_v1.json.",
    )

    @field_validator("weights")
    @classmethod
    def _weights_sum_to_one(cls, v: Dict[str, float]) -> Dict[str, float]:
        total = sum(v.values())
        if not (0.999 <= total <= 1.001):
            raise ValueError(f"Scoring weights must sum to 1.0, got {total:.4f}")
        required = {"sentiment", "volume", "geo_cluster", "trend"}
        missing = required - v.keys()
        if missing:
            raise ValueError(f"Missing required weight keys: {missing}")
        return v


# Module-level singleton — import this everywhere.
settings = Settings()
