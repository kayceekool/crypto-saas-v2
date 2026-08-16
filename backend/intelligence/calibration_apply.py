from dataclasses import dataclass

from backend.intelligence.calibration import (
    CalibrationProfile,
)


@dataclass(frozen=True)
class AdjustedSignal:
    """
    Result of applying a bounded calibration profile
    to an existing signal.

    This object contains values only. It does not
    execute trades or modify the original signal.
    """

    original_score: float

    adjusted_score: float

    original_confidence: float

    adjusted_confidence: float

    original_risk: float

    adjusted_risk: float

    def to_dict(self) -> dict:
        return {
            "original_score": (
                self.original_score
            ),
            "adjusted_score": (
                self.adjusted_score
            ),
            "original_confidence": (
                self.original_confidence
            ),
            "adjusted_confidence": (
                self.adjusted_confidence
            ),
            "original_risk": (
                self.original_risk
            ),
            "adjusted_risk": (
                self.adjusted_risk
            ),
        }


class CalibrationApplier:
    """
    Applies a CalibrationProfile to signal values.

    All values are bounded to prevent feedback from
    creating extreme intelligence changes.
    """

    MIN_SCORE = 0.0
    MAX_SCORE = 1000.0

    MIN_CONFIDENCE = 0.0
    MAX_CONFIDENCE = 100.0

    MIN_RISK = 0.0
    MAX_RISK = 100.0

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
    def apply(
        cls,
        score: float,
        confidence: float,
        risk: float,
        profile: CalibrationProfile,
    ) -> AdjustedSignal:

        original_score = float(score)

        original_confidence = float(
            confidence
        )

        original_risk = float(risk)

        adjusted_score = cls._clamp(
            original_score
            + profile.score_adjustment,
            cls.MIN_SCORE,
            cls.MAX_SCORE,
        )

        adjusted_confidence = cls._clamp(
            original_confidence
            * profile.confidence_multiplier,
            cls.MIN_CONFIDENCE,
            cls.MAX_CONFIDENCE,
        )

        adjusted_risk = cls._clamp(
            original_risk
            + profile.risk_adjustment,
            cls.MIN_RISK,
            cls.MAX_RISK,
        )

        return AdjustedSignal(
            original_score=round(
                original_score,
                4,
            ),
            adjusted_score=round(
                adjusted_score,
                4,
            ),
            original_confidence=round(
                original_confidence,
                4,
            ),
            adjusted_confidence=round(
                adjusted_confidence,
                4,
            ),
            original_risk=round(
                original_risk,
                4,
            ),
            adjusted_risk=round(
                adjusted_risk,
                4,
            ),
        )