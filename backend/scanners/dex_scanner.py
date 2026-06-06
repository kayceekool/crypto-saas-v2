import httpx

from core.config import DEXSCREENER_URL

from services.scoring_engine import (
    ScoringEngine
)

from intelligence.adaptive_ranking import (
    AdaptiveRanking
)

from intelligence.adaptive_confidence import (
    AdaptiveConfidence
)

from intelligence.master_ai import (
    MasterAI
)

from services.rating_engine import (
    RatingEngine
)


class DexScanner:

    async def search(
        self,
        query: str
    ):

        async with httpx.AsyncClient() as client:

            r = await client.get(
                f"{DEXSCREENER_URL}?q={query}",
                timeout=20
            )

            data = r.json()

            pairs = data.get(
                "pairs",
                []
            )

            results = []

            for pair in pairs:

                try:

                    token = {
                        "symbol": (
                            pair.get(
                                "baseToken",
                                {}
                            ).get(
                                "symbol",
                                "UNKNOWN"
                            )
                        ),

                        "address": (
                            pair.get(
                                "pairAddress",
                                ""
                            )
                        ),

                        "price": float(
                            pair.get(
                                "priceUsd",
                                0
                            ) or 0
                        ),

                        "liquidity": float(
                            pair.get(
                                "liquidity",
                                {}
                            ).get(
                                "usd",
                                0
                            ) or 0
                        ),

                        "volume": float(
                            pair.get(
                                "volume",
                                {}
                            ).get(
                                "h24",
                                0
                            ) or 0
                        ),

                        "score": 0,
                        "confidence": 50
                    }

                    token["score"] = (
                        ScoringEngine.calculate(
                            token
                        )
                    )

                    token = (
                        AdaptiveRanking.boost(
                            token
                        )
                    )

                    token = (
                        MasterAI.enhance(
                            token
                        )
                    )

token["rating"] = (
    RatingEngine.rate(
        token["score"]
    )
)
                    token["confidence"] = (
                        AdaptiveConfidence.adjust(
                            token.get(
                                "confidence",
                                50
                            )
                        )
                    )

                    results.append(
                        token
                    )

                except Exception as e:

                    print(
                        f"DexScanner error: {e}"
                    )

            return results