from dataclasses import dataclass
from datetime import datetime


@dataclass
class SignalHistoryRecord:

    token_address: str
    symbol: str

    action: str

    score: float
    confidence: float

    risk: str
    reason: str

    price_at_signal: float = 0.0

    outcome: str | None = None

    pnl: float | None = None

    created_at: datetime | None = None

    resolved_at: datetime | None = None

    def __post_init__(self):

        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def resolve(
        self,
        outcome: str,
        pnl: float,
    ):

        self.outcome = outcome

        self.pnl = float(pnl)

        self.resolved_at = (
            datetime.utcnow()
        )

    def to_dict(self) -> dict:

        return {
            "token_address": (
                self.token_address
            ),
            "symbol": self.symbol,
            "action": self.action,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "reason": self.reason,
            "price_at_signal": (
                self.price_at_signal
            ),
            "outcome": self.outcome,
            "pnl": self.pnl,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "resolved_at": (
                self.resolved_at.isoformat()
                if self.resolved_at
                else None
            ),
        }