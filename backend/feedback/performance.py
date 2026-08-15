from dataclasses import dataclass

from backend.signals.persistence import (
    SignalHistoryRecord,
)


@dataclass
class PerformanceMetrics:

    total_signals: int

    resolved_signals: int

    unresolved_signals: int

    wins: int

    losses: int

    win_rate: float

    average_pnl: float

    total_pnl: float

    buy_signals: int

    strong_buy_signals: int

    watch_signals: int

    avoid_signals: int

    hold_signals: int

    average_confidence: float

    def to_dict(self) -> dict:

        return {
            "total_signals": (
                self.total_signals
            ),
            "resolved_signals": (
                self.resolved_signals
            ),
            "unresolved_signals": (
                self.unresolved_signals
            ),
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.win_rate,
            "average_pnl": self.average_pnl,
            "total_pnl": self.total_pnl,
            "buy_signals": (
                self.buy_signals
            ),
            "strong_buy_signals": (
                self.strong_buy_signals
            ),
            "watch_signals": (
                self.watch_signals
            ),
            "avoid_signals": (
                self.avoid_signals
            ),
            "hold_signals": (
                self.hold_signals
            ),
            "average_confidence": (
                self.average_confidence
            ),
        }


class PerformanceEngine:

    @staticmethod
    def _round(
        value: float,
    ) -> float:

        return round(
            float(value),
            4,
        )

    @classmethod
    def calculate(
        cls,
        records: list[
            SignalHistoryRecord
        ],
    ) -> PerformanceMetrics:

        total = len(records)

        resolved = [
            record
            for record in records
            if record.outcome is not None
        ]

        unresolved = total - len(resolved)

        wins = sum(
            1
            for record in resolved
            if str(
                record.outcome
            ).upper()
            == "WIN"
        )

        losses = sum(
            1
            for record in resolved
            if str(
                record.outcome
            ).upper()
            == "LOSS"
        )

        pnl_values = [
            float(record.pnl)
            for record in resolved
            if record.pnl is not None
        ]

        total_pnl = sum(
            pnl_values
        )

        average_pnl = (
            total_pnl / len(pnl_values)
            if pnl_values
            else 0.0
        )

        win_rate = (
            (wins / len(resolved))
            * 100.0
            if resolved
            else 0.0
        )

        buy_signals = sum(
            1
            for record in records
            if str(
                record.action
            ).upper()
            == "BUY"
        )

        strong_buy_signals = sum(
            1
            for record in records
            if str(
                record.action
            ).upper()
            == "STRONG_BUY"
        )

        watch_signals = sum(
            1
            for record in records
            if str(
                record.action
            ).upper()
            == "WATCH"
        )

        avoid_signals = sum(
            1
            for record in records
            if str(
                record.action
            ).upper()
            == "AVOID"
        )

        hold_signals = sum(
            1
            for record in records
            if str(
                record.action
            ).upper()
            == "HOLD"
        )

        confidence_values = [
            float(
                record.confidence
            )
            for record in records
        ]

        average_confidence = (
            sum(confidence_values)
            / len(confidence_values)
            if confidence_values
            else 0.0
        )

        return PerformanceMetrics(
            total_signals=total,
            resolved_signals=len(resolved),
            unresolved_signals=unresolved,
            wins=wins,
            losses=losses,
            win_rate=cls._round(
                win_rate
            ),
            average_pnl=cls._round(
                average_pnl
            ),
            total_pnl=cls._round(
                total_pnl
            ),
            buy_signals=buy_signals,
            strong_buy_signals=(
                strong_buy_signals
            ),
            watch_signals=watch_signals,
            avoid_signals=avoid_signals,
            hold_signals=hold_signals,
            average_confidence=cls._round(
                average_confidence
            ),
        )

    @classmethod
    def calculate_by_action(
        cls,
        records: list[
            SignalHistoryRecord
        ],
    ) -> dict[str, PerformanceMetrics]:

        actions = {
            str(
                record.action
            ).upper()
            for record in records
        }

        return {
            action: cls.calculate(
                [
                    record
                    for record in records
                    if str(
                        record.action
                    ).upper()
                    == action
                ]
            )
            for action in sorted(actions)
        }

    @classmethod
    def calculate_by_confidence(
        cls,
        records: list[
            SignalHistoryRecord
        ],
    ) -> dict[str, PerformanceMetrics]:

        buckets = {
            "LOW": [],
            "MEDIUM": [],
            "HIGH": [],
        }

        for record in records:

            confidence = float(
                record.confidence
            )

            if confidence < 50:

                buckets["LOW"].append(
                    record
                )

            elif confidence < 75:

                buckets["MEDIUM"].append(
                    record
                )

            else:

                buckets["HIGH"].append(
                    record
                )

        return {
            bucket: cls.calculate(
                bucket_records
            )
            for bucket, bucket_records
            in buckets.items()
        }