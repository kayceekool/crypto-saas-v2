from services.ranking_engine import (
    RankingEngine
)

from services.alert_engine import (
    AlertEngine
)


class IntelligenceHub:

    @staticmethod
    async def process(tokens):

        ranked = RankingEngine.rank(
            tokens
        )

        if ranked:

            await AlertEngine.broadcast(
                {
                    "type":
                    "top_token",

                    "token":
                    ranked[0]
                }
            )

        return ranked