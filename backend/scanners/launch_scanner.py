from backend.core.provider_registry import (
    ProviderRegistry,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.scanners.base import (
    BaseScanner,
)


class LaunchScanner(BaseScanner):

    name = "launch"

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

        pumpfun = self.registry.get(
            "pumpfun"
        )

        if pumpfun is not None:

            try:

                results.extend(
                    await pumpfun.search(
                        query
                    )
                )

            except Exception as exc:

                print(
                    f"LaunchScanner Pump.fun "
                    f"error: {exc}"
                )

        # Other providers may also expose
        # launch information in future packages.

        return self._filter_recent(
            results
        )

    @staticmethod
    def _filter_recent(
        tokens: list[TokenMarketData],
    ) -> list[TokenMarketData]:

        recent = []

        for token in tokens:

            if token.age_hours < 1:

                recent.append(
                    token
                )

        return recent