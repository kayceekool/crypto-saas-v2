from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class IntelligenceRecord:

    token_address: str
    symbol: str

    score: float
    confidence: float

    pattern: str
    risk: str
    signal: str

    price: float = 0.0
    liquidity: float = 0.0
    volume: float = 0.0

    created_at: datetime | None = None

    metadata: dict[str, Any] | None = None

    def __post_init__(self):

        if self.created_at is None:
            self.created_at = datetime.utcnow()

        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:

        return {
            "token_address": self.token_address,
            "symbol": self.symbol,
            "score": self.score,
            "confidence": self.confidence,
            "pattern": self.pattern,
            "risk": self.risk,
            "signal": self.signal,
            "price": self.price,
            "liquidity": self.liquidity,
            "volume": self.volume,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }