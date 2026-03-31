from __future__ import annotations

import json
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LEXICON_PATH = PROJECT_ROOT / "data" / "sample" / "lexicons" / "crisis_terms_v1.json"
BASE_DIR = Path(__file__).resolve().parents[2]


def load_crisis_terms() -> list[str]:
    with LEXICON_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AI4MH_", env_file=".env", extra="ignore")

    app_name: str = "AI4MH API"
    api_prefix: str = "/api"
    max_posts: int = Field(default=500, ge=1)
    default_ingest_batch_size: int = Field(default=30, ge=1, le=500)
    bootstrap_batch_size: int = Field(default=120, ge=1, le=1000)
    sqlite_path: str = "ai4mh.db"
    allowed_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:4173",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:4173",
            "http://127.0.0.1:5173",
        ]
    )
    weights: dict[str, float] = Field(
        default={
            "sentiment": 0.35,
            "volume": 0.30,
            "geo_cluster": 0.20,
            "trend": 0.15,
        }
    )
    escalation_thresholds: dict[str, float] = Field(
        default={
            "crisis_score": 0.70,
            "confidence": 0.60,
            "min_posts": 10,
            "max_bot_ratio": 0.25,
        }
    )
    crisis_terms: list[str] = Field(default_factory=load_crisis_terms)

    @field_validator("weights")
    @classmethod
    def validate_weights(cls, value: dict[str, float]) -> dict[str, float]:
        required = {"sentiment", "volume", "geo_cluster", "trend"}
        missing = required.difference(value)
        if missing:
            raise ValueError(f"missing score weights: {sorted(missing)}")

        total = round(sum(value.values()), 6)
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"weights must sum to 1.0, got {total:.3f}")
        return value


settings = Settings()
