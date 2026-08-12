from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenMarketData:

    symbol: str = "UNKNOWN"

    address: str = ""

    chain: str = "solana"

    price_usd: float = 0.0

    liquidity_usd: float = 0.0

    volume_24h_usd: float = 0.0

    market_cap_usd: float = 0.0

    pair_address: str = ""

    source: str = ""

    age_hours: float = 999.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict:

        return {
            "symbol": self.symbol,
            "address": self.address,
            "chain": self.chain,
            "price_usd": self.price_usd,
            "liquidity_usd": self.liquidity_usd,
            "volume_24h_usd": self.volume_24h_usd,
            "market_cap_usd": self.market_cap_usd,
            "pair_address": self.pair_address,
            "source": self.source,
            "age_hours": self.age_hours,
            "metadata": self.metadata,
        }