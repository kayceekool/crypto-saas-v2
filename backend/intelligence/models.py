from dataclasses import dataclass, field
from typing import Any

from backend.providers.models import (
    TokenMarketData,
)


@dataclass
class IntelligenceResult:

    token: TokenMarketData

    base_score: float = 0.0

    pattern_adjustment: float = 0.0

    launch_adjustment: float = 0.0

    migration_adjustment: float = 0.0

    final_score: float = 0.0

    confidence: float = 50.0

    pattern: str = "NORMAL"

    risk: str = "UNKNOWN"

    signal: str = "WATCH"

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict:

        return {
            "token": self.token.to_dict(),
            "base_score": self.base_score,
            "pattern_adjustment": (
                self.pattern_adjustment
            ),
            "launch_adjustment": (
                self.launch_adjustment
            ),
            "migration_adjustment": (
                self.migration_adjustment
            ),
            "final_score": self.final_score,
            "confidence": self.confidence,
            "pattern": self.pattern,
            "risk": self.risk,
            "signal": self.signal,
            "metadata": self.metadata,
        }