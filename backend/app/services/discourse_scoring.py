from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)

InterventionResult = Literal["success", "partial", "fail"]

# Keywords derived from cognitron-game's mockAnalyst logic
EVIDENCE_KEYWORDS = {"evidence", "source", "data", "study", "research"}
EMPATHY_KEYWORDS = {"why", "feel", "understand", "perspective", "experience"}


@dataclass
class DiscourseScore:
    intervention: str
    result: InterventionResult
    confidence: float


class DiscourseScoringService:
    """
    Ported from Cognitron-Game.
    Scores participant interventions designed to break echo chamber patterns.
    """

    def score_intervention(self, text: str, syndrome: str) -> DiscourseScore:
        lowered = (text or "").lower()

        # Weighted keyword analysis
        evidence_hits = sum(1 for k in EVIDENCE_KEYWORDS if k in lowered)
        empathy_hits = sum(1 for k in EMPATHY_KEYWORDS if k in lowered)

        # Base score calculation
        score = (evidence_hits * 0.4) + (empathy_hits * 0.3)

        # Determine result based on thresholds
        if score >= 0.6:
            result: InterventionResult = "success"
        elif score >= 0.3:
            result: InterventionResult = "partial"
        else:
            result: InterventionResult = "fail"

        logger.info(
            "Scored intervention",
            extra={
                "syndrome": syndrome,
                "score": score,
                "result": result,
                "evidence_hits": evidence_hits,
                "empathy_hits": empathy_hits,
            },
        )

        return DiscourseScore(
            intervention=text, result=result, confidence=round(min(score, 1.0), 2)
        )
