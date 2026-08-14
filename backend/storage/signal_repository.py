from datetime import datetime

from backend.signals.models import (
    SignalDecision,
)

from backend.signals.persistence import (
    SignalHistoryRecord,
)


class SignalRepository:

    @staticmethod
    def from_decision(
        decision: SignalDecision,
        price: float = 0.0,
    ) -> SignalHistoryRecord:

        return SignalHistoryRecord(
            token_address=(
                decision.token_address
            ),
            symbol=decision.symbol,
            action=decision.action,
            score=decision.score,
            confidence=decision.confidence,
            risk=decision.risk,
            reason=decision.reason,
            price_at_signal=price,
            created_at=(
                decision.created_at
            ),
        )

    @classmethod
    def from_decisions(
        cls,
        decisions: list[
            SignalDecision
        ],
    ) -> list[
        SignalHistoryRecord
    ]:

        return [
            cls.from_decision(
                decision
            )
            for decision in decisions
        ]

    @staticmethod
    def resolve(
        record: SignalHistoryRecord,
        outcome: str,
        pnl: float,
    ) -> SignalHistoryRecord:

        record.resolve(
            outcome=outcome,
            pnl=pnl,
        )

        return record

    @staticmethod
    def serialize(
        records: list[
            SignalHistoryRecord
        ],
    ) -> list[dict]:

        return [
            record.to_dict()
            for record in records
        ]