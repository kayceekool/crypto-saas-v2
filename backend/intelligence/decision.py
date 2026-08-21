from dataclasses import dataclass

from backend.intelligence.calibration_apply import (
    AdjustedSignal,
)


@dataclass(frozen=True)
class IntelligenceDecision:
    """
    Final classification of an adjusted signal.

    This is a decision/classification object only.
    It does not execute trades or modify the signal.
    """

    decision: str

    score: float

    confidence: float

    risk: float

    reason: str

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "reason": self.reason,
        }


class IntelligenceDecisionEngine:
    """
    Converts bounded adjusted signal values into a
    conservative intelligence classification.

    Decision hierarchy:

        STRONG
        ACCEPT
        WATCH
        REJECT

    Risk always has priority over score.
    """

    STRONG_SCORE = 800.0
    STRONG_CONFIDENCE = 75.0
    STRONG_MAX_RISK = 30.0

    ACCEPT_SCORE = 650.0
    ACCEPT_CONFIDENCE = 60.0
    ACCEPT_MAX_RISK = 50.0

    WATCH_SCORE = 500.0
    WATCH_CONFIDENCE = 45.0
    WATCH_MAX_RISK = 70.0

    @staticmethod
    def _normalise(
        value: float,
    ) -> float:
        return float(value)

    @classmethod
    def evaluate(
        cls,
        signal: AdjustedSignal,
    ) -> IntelligenceDecision:
        score = cls._normalise(
            signal.adjusted_score
        )

        confidence = cls._normalise(
            signal.adjusted_confidence
        )

        risk = cls._normalise(
            signal.adjusted_risk
        )

        # Risk takes priority over all positive
        # classifications.
        if risk > cls.WATCH_MAX_RISK:
            return IntelligenceDecision(
                decision="REJECT",
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Risk exceeds the maximum "
                    "acceptable intelligence threshold."
                ),
            )

        if (
            score >= cls.STRONG_SCORE
            and confidence
            >= cls.STRONG_CONFIDENCE
            and risk
            <= cls.STRONG_MAX_RISK
        ):
            return IntelligenceDecision(
                decision="STRONG",
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Score and confidence are strong "
                    "while risk remains low."
                ),
            )

        if (
            score >= cls.ACCEPT_SCORE
            and confidence
            >= cls.ACCEPT_CONFIDENCE
            and risk
            <= cls.ACCEPT_MAX_RISK
        ):
            return IntelligenceDecision(
                decision="ACCEPT",
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Score and confidence meet the "
                    "acceptance thresholds."
                ),
            )

        if (
            score >= cls.WATCH_SCORE
            and confidence
            >= cls.WATCH_CONFIDENCE
            and risk
            <= cls.WATCH_MAX_RISK
        ):
            return IntelligenceDecision(
                decision="WATCH",
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Signal shows potential but does "
                    "not yet meet the acceptance threshold."
                ),
            )

        return IntelligenceDecision(
            decision="REJECT",
            score=score,
            confidence=confidence,
            risk=risk,
            reason=(
                "Signal does not meet the minimum "
                "intelligence thresholds."
            ),
        )