from dataclasses import dataclass

from backend.feedback.performance import (
    PerformanceEngine,
)

from backend.feedback.recommendations import (
    FeedbackEngine,
    FeedbackRecommendation,
)

from backend.intelligence.calibration import (
    CalibrationEngine,
    CalibrationProfile,
)

from backend.intelligence.calibration_apply import (
    AdjustedSignal,
    CalibrationApplier,
)


@dataclass(frozen=True)
class IntelligenceResult:
    """
    Complete result of the intelligence feedback pipeline.

    This object contains the recommendation, calibration
    profile, and adjusted signal values.

    It does not execute trades.
    """

    recommendation: FeedbackRecommendation

    calibration: CalibrationProfile

    adjusted_signal: AdjustedSignal

    def to_dict(self) -> dict:
        return {
            "recommendation": (
                self.recommendation.to_dict()
            ),
            "calibration": (
                self.calibration.to_dict()
            ),
            "adjusted_signal": (
                self.adjusted_signal.to_dict()
            ),
        }


class IntelligencePipeline:
    """
    Orchestrates the complete feedback-to-calibration flow.

    Flow:

        historical signals
            ↓
        performance metrics
            ↓
        feedback recommendation
            ↓
        calibration profile
            ↓
        adjusted signal
    """

    @classmethod
    def evaluate(
        cls,
        historical_records,
        score: float,
        confidence: float,
        risk: float,
    ) -> IntelligenceResult:
        """
        Evaluate historical performance and apply the
        resulting bounded calibration to a signal.

        The historical records are never modified.
        """

        metrics = PerformanceEngine.calculate(
            historical_records
        )

        recommendation = (
            FeedbackEngine.evaluate(
                metrics
            )
        )

        calibration = (
            CalibrationEngine.from_feedback(
                recommendation
            )
        )

        adjusted_signal = (
            CalibrationApplier.apply(
                score=score,
                confidence=confidence,
                risk=risk,
                profile=calibration,
            )
        )

        return IntelligenceResult(
            recommendation=recommendation,
            calibration=calibration,
            adjusted_signal=adjusted_signal,
        )