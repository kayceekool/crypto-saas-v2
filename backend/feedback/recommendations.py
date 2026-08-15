from dataclasses import dataclass

from backend.feedback.performance import (
    PerformanceMetrics,
)


@dataclass(frozen=True)
class FeedbackRecommendation:
    """
    A read-only recommendation produced from
    historical signal performance.

    This object does not change trading settings
    or execute trades.
    """

    status: str

    confidence: float

    message: str

    suggested_action: str

    win_rate: float

    average_pnl: float

    total_pnl: float

    resolved_signals: int

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "confidence": self.confidence,
            "message": self.message,
            "suggested_action": (
                self.suggested_action
            ),
            "win_rate": self.win_rate,
            "average_pnl": self.average_pnl,
            "total_pnl": self.total_pnl,
            "resolved_signals": (
                self.resolved_signals
            ),
        }


class FeedbackEngine:
    """
    Converts historical performance metrics into
    conservative intelligence recommendations.

    No trading execution occurs here.
    """

    MIN_RESOLVED_FOR_CONFIDENT = 10

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ) -> float:
        return max(
            minimum,
            min(maximum, float(value)),
        )

    @classmethod
    def evaluate(
        cls,
        metrics: PerformanceMetrics,
    ) -> FeedbackRecommendation:

        resolved = metrics.resolved_signals

        if resolved == 0:

            return FeedbackRecommendation(
                status="INSUFFICIENT_DATA",
                confidence=0.0,
                message=(
                    "There are no resolved signals "
                    "available for feedback."
                ),
                suggested_action=(
                    "COLLECT_MORE_OUTCOMES"
                ),
                win_rate=metrics.win_rate,
                average_pnl=metrics.average_pnl,
                total_pnl=metrics.total_pnl,
                resolved_signals=resolved,
            )

        if resolved < cls.MIN_RESOLVED_FOR_CONFIDENT:

            confidence = cls._clamp(
                resolved * 10.0
            )

            return FeedbackRecommendation(
                status="LIMITED_DATA",
                confidence=confidence,
                message=(
                    "Historical outcomes are available, "
                    "but more resolved signals are needed "
                    "before making a strong adjustment."
                ),
                suggested_action=(
                    "CONTINUE_OBSERVATION"
                ),
                win_rate=metrics.win_rate,
                average_pnl=metrics.average_pnl,
                total_pnl=metrics.total_pnl,
                resolved_signals=resolved,
            )

        if (
            metrics.win_rate >= 70.0
            and metrics.average_pnl > 0
        ):

            confidence = cls._clamp(
                metrics.win_rate
            )

            return FeedbackRecommendation(
                status="POSITIVE",
                confidence=confidence,
                message=(
                    "Historical performance is positive. "
                    "The current signal configuration "
                    "is showing favorable results."
                ),
                suggested_action=(
                    "MAINTAIN_CONFIGURATION"
                ),
                win_rate=metrics.win_rate,
                average_pnl=metrics.average_pnl,
                total_pnl=metrics.total_pnl,
                resolved_signals=resolved,
            )

        if (
            metrics.win_rate < 40.0
            or metrics.average_pnl < 0
        ):

            confidence = cls._clamp(
                100.0 - metrics.win_rate
            )

            return FeedbackRecommendation(
                status="NEGATIVE",
                confidence=confidence,
                message=(
                    "Historical performance is weak. "
                    "The signal configuration should "
                    "be reviewed before increasing "
                    "confidence."
                ),
                suggested_action=(
                    "REVIEW_CONFIGURATION"
                ),
                win_rate=metrics.win_rate,
                average_pnl=metrics.average_pnl,
                total_pnl=metrics.total_pnl,
                resolved_signals=resolved,
            )

        return FeedbackRecommendation(
            status="NEUTRAL",
            confidence=50.0,
            message=(
                "Historical performance is mixed. "
                "Continue collecting outcomes before "
                "making a significant adjustment."
            ),
            suggested_action=(
                "CONTINUE_OBSERVATION"
            ),
            win_rate=metrics.win_rate,
            average_pnl=metrics.average_pnl,
            total_pnl=metrics.total_pnl,
            resolved_signals=resolved,
        )