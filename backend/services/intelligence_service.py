from backend.intelligence.master import (
    MasterAI,
)

from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.providers.models import (
    TokenMarketData,
)


class IntelligenceService:

    def __init__(
        self,
        engine: MasterAI | None = None,
    ):

        self.engine = (
            engine
            or
            MasterAI()
        )

    def analyze(
        self,
        token: TokenMarketData,
    ) -> IntelligenceResult:

        return self.engine.analyze(
            token
        )

    def analyze_many(
        self,
        tokens: list[TokenMarketData],
    ) -> list[IntelligenceResult]:

        return [
            self.analyze(token)
            for token in tokens
        ]

    def rank(
        self,
        tokens: list[TokenMarketData],
    ) -> list[IntelligenceResult]:

        results = self.analyze_many(
            tokens
        )

        return sorted(
            results,
            key=lambda result:
                result.final_score,
            reverse=True,
        )