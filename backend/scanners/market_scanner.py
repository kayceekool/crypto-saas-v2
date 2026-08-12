from backend.core.provider_registry import (
    ProviderRegistry,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.scanners.base import (
    BaseScanner,
)


class MarketScanner(BaseScanner):

    name = "market"

    def __init__(
        self,
        registry: ProviderRegistry,
    ):

        self.registry = registry

    async def scan(
        self,
        query: str = "SOL",
    ) -> list[TokenMarketData]:

        results: list[
            TokenMarketData
        ] = []

        for provider in self.registry.all():

            try:

                tokens = await provider.search(
                    query
                )

                results.extend(
                    tokens
                )

            except Exception as exc:

                print(
                    f"MarketScanner provider "
                    f"{provider.name} error: {exc}"
                )

        return self._deduplicate(
            results
        )

    @staticmethod
    def _deduplicate(
        tokens: list[TokenMarketData],
    ) -> list[TokenMarketData]:

        unique = {}

        for token in tokens:

            key = (
                token.address
                or
                token.pair_address
                or
                f"{token.source}:{token.symbol}"
            )

            if key not in unique:

                unique[key] = token

        return list(
            unique.values()
        )