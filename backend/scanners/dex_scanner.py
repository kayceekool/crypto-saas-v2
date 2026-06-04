import httpx

from services.scoring_engine import (
    ScoringEngine
)

from intelligence.adaptive_ranking import (
    AdaptiveRanking
)

from intelligence.adaptive_confidence import (
    AdaptiveConfidence
)

from core.config import (
    DEXSCREENER_URL
)


class DexScanner:

    async def search(
        self,
        query
    ):

        async with httpx.AsyncClient() as client:

            r = await client.get(
                f"{DEXSCREENER_URL}?q={query}"
            )

            data = r.json()

            return data