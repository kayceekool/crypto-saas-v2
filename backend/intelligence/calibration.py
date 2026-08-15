from dataclasses import dataclass

from backend.feedback.recommendations import (
    FeedbackRecommendation,
)


@dataclass(frozen=True)
class CalibrationProfile:
    """
    Bounded intelligence-calibration parameters.

    These values describe how strongly the future
    intelligence layer may adjust its confidence.

    This class does not execute trades and does not
    directly modify the signal engine.
    """

    confidence_multiplier: float

    score_adjustment: float

    risk_adjustment: float

    status: str

    reason: str

    def to_dict(self) -> dict:
        return {
            "confidence_multiplier": (
                self.confidence_multiplier
            ),
            "score_adjustment": (
                self.score_adjustment
            ),
            "risk_adjustment": (
                self.risk_adjustment
            ),
            "status": self.status,
            "reason": self.reason,
        }


class CalibrationEngine:
    """
    Converts feedback recommendations into conservative,
    bounded calibration parameters.

    Calibration is intentionally limited so that a small
    amount of historical data cannot cause extreme changes.
    """

    MIN_MULTIPLIER = 0.90
    MAX_MULTIPLIER = 1.10

    MIN_SCORE_ADJUSTMENT = -5.0
    MAX_SCORE_ADJUSTMENT = 5.0

    MIN_RISK_ADJUSTMENT = -5.0
    MAX_RISK_ADJUSTMENT = 5.0

    @staticmethod
    def _clamp(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        return max(
            minimum,
            min(maximum, float(value)),
        )

    @classmethod
    def from_feedback(
        cls,
        recommendation: FeedbackRecommendation,
    ) -> CalibrationProfile:

        status = (
            recommendation.status
        )

        if status == "INSUFFICIENT_DATA":

            return CalibrationProfile(
                confidence_multiplier=1.0,
                score_adjustment=0.0,
                risk_adjustment=0.0,
                status="NEUTRAL",
                reason=(
                    "Insufficient historical data. "
                    "No calibration is applied."
                ),
            )

        if status == "LIMITED_DATA":

            return CalibrationProfile(
                confidence_multiplier=1.0,
                score_adjustment=0.0,
                risk_adjustment=0.0,
                status="OBSERVE",
                reason=(
                    "Historical data is limited. "
                    "Continue observation before "
                    "calibrating intelligence."
                ),
            )

        if status == "POSITIVE":

            strength = cls._clamp(
                recommendation.confidence
                / 100.0,
                0.0,
                1.0,
            )

            multiplier = cls._clamp(
                1.0
                + (0.10 * strength),
                cls.MIN_MULTIPLIER,
                cls.MAX_MULTIPLIER,
            )

            score_adjustment = cls._clamp(
                5.0 * strength,
                cls.MIN_SCORE_ADJUSTMENT,
                cls.MAX_SCORE_ADJUSTMENT,
            )

            risk_adjustment = cls._clamp(
                -2.0 * strength,
                cls.MIN_RISK_ADJUSTMENT,
                cls.MAX_RISK_ADJUSTMENT,
            )

            return CalibrationProfile(
                confidence_multiplier=round(
                    multiplier,
                    4,
                ),
                score_adjustment=round(
                    score_adjustment,
                    4,
                ),
                risk_adjustment=round(
                    risk_adjustment,
                    4,
                ),
                status="POSITIVE",
                reason=(
                    "Positive historical performance "
                    "supports a small bounded increase "
                    "in confidence."
                ),
            )

        if status == "NEGATIVE":

            strength = cls._clamp(
                recommendation.confidence
                / 100.0,
                0.0,
                1.0,
            )

            multiplier = cls._clamp(
                1.0
                - (0.10 * strength),
                cls.MIN_MULTIPLIER,
                cls.MAX_MULTIPLIER,
            )

            score_adjustment = cls._clamp(
                -5.0 * strength,
                cls.MIN_SCORE_ADJUSTMENT,
                cls.MAX_SCORE_ADJUSTMENT,
            )

            risk_adjustment = cls._clamp(
                2.0 * strength,
                cls.MIN_RISK_ADJUSTMENT,
                cls.MAX_RISK_ADJUSTMENT,
            )

            return CalibrationProfile(
                confidence_multiplier=round(
                    multiplier,
                    4,
                ),
                score_adjustment=round(
                    score_adjustment,
                    4,
                ),
                risk_adjustment=round(
                    risk_adjustment,
                    4,
                ),
                status="NEGATIVE",
                reason=(
                    "Weak historical performance "
                    "supports a small bounded reduction "
                    "in confidence."
                ),
            )

        return CalibrationProfile(
            confidence_multiplier=1.0,
            score_adjustment=0.0,
            risk_adjustment=0.0,
            status="NEUTRAL",
            reason=(
                "Historical performance is mixed. "
                "No significant calibration is applied."
            ),
        )