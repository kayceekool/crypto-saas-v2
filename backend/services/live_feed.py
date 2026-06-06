# backend/services/live_feed.py

from scanners.dex_scanner import (
    DexScanner
)

from services.intelligence_hub import (
    IntelligenceHub
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

        return ranked