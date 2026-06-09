from services.ranking_engine import (
    RankingEngine
)

from services.alert_engine import (
    AlertEngine
)

from services.alert_classifier import (
    AlertClassifier
)


class IntelligenceHub:

    @staticmethod
    async def process(tokens):

        ranked = RankingEngine.rank(
            tokens
        )

        if ranked:

            top = ranked[0]

            await AlertEngine.broadcast(
                {
                    "type":
                        "top_token",

                    "severity":
                        AlertClassifier.level(
                            top
                        ),

                    "token":
                        top
                }
            )

        return ranked