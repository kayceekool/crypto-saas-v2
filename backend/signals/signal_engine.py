from datetime import datetime

from backend.intelligence.persistence import (
    IntelligenceRecord,
)

from backend.signals.models import (
    SignalDecision,
)


class SignalEngine:

    STRONG_SCORE = 800

    BUY_SCORE = 650

    WATCH_SCORE = 450

    HIGH_CONFIDENCE = 70

    MEDIUM_CONFIDENCE = 50

    @classmethod
    def evaluate(
        cls,
        record: IntelligenceRecord,
    ) -> SignalDecision:

        score = float(
            record.score
        )

        confidence = float(
            record.confidence
        )

        risk = (
            record.risk
            or "UNKNOWN"
        ).upper()

        signal = (
            record.signal
            or ""
        ).upper()

        action = "HOLD"

        reason = (
            "Insufficient conditions "
            "for an actionable signal."
        )

        if risk == "HIGH":

            action = "AVOID"

            reason = (
                "Risk level is too high "
                "for a positive signal."
            )

        elif (
            score >= cls.STRONG_SCORE
            and confidence >= cls.HIGH_CONFIDENCE
        ):

            action = "STRONG_BUY"

            reason = (
                "Very strong intelligence "
                "score and confidence."
            )

        elif (
            score >= cls.BUY_SCORE
            and confidence >= cls.MEDIUM_CONFIDENCE
        ):

            action = "BUY"

            reason = (
                "Score and confidence "
                "meet the buy threshold."
            )

        elif score >= cls.WATCH_SCORE:

            action = "WATCH"

            reason = (
                "Token has sufficient "
                "intelligence strength "
                "for monitoring."
            )

        elif signal in {
            "STRONG",
            "BUY",
        } and confidence >= cls.MEDIUM_CONFIDENCE:

            action = "WATCH"

            reason = (
                "Existing intelligence signal "
                "supports continued monitoring."
            )

        return SignalDecision(
            token_address=(
                record.token_address
            ),
            symbol=record.symbol,
            action=action,
            score=score,
            confidence=confidence,
            risk=risk,
            reason=reason,
            created_at=datetime.utcnow(),
        )

    @classmethod
    def evaluate_many(
        cls,
        records: list[
            IntelligenceRecord
        ],
    ) -> list[SignalDecision]:

        return [
            cls.evaluate(record)
            for record in records
        ]