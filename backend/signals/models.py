from dataclasses import dataclass
from datetime import datetime


@dataclass
class SignalDecision:

    token_address: str

    symbol: str

    action: str

    score: float

    confidence: float

    risk: str

    reason: str

    created_at: datetime

    def to_dict(self) -> dict:

        return {
            "token_address": self.token_address,
            "symbol": self.symbol,
            "action": self.action,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "reason": self.reason,
            "created_at": (
                self.created_at.isoformat()
            ),
        }