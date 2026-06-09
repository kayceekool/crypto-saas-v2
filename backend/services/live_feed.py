from scanners.dex_scanner import (
    DexScanner
)

from services.intelligence_hub import (
    IntelligenceHub
)

from services.market_state import (
    MarketState
)

from core.database import (
    AsyncSessionLocal
)

from storage.token_repository import (
    TokenRepository
)


class LiveFeed:

    scanner = DexScanner()

    @classmethod
    async def update(cls):

        tokens = await cls.scanner.search(
            "sol"
        )

        ranked = await (
            IntelligenceHub.process(
                tokens
            )
        )

        MarketState.rankings = ranked

        if ranked:

            MarketState.top_token = (
                ranked[0]
            )

        return ranked