from backend.core.provider_registry import (
    ProviderRegistry,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.scanners.launch_scanner import (
    LaunchScanner,
)

from backend.scanners.market_scanner import (
    MarketScanner,
)


class ScannerManager:

    def __init__(
        self,
        registry: ProviderRegistry,
    ):

        self.registry = registry

        self.market = MarketScanner(
            registry
        )

        self.launch = LaunchScanner(
            registry
        )

    async def market_scan(
        self,
        query: str = "SOL",
    ) -> list[TokenMarketData]:

        return await self.market.scan(
            query
        )

    async def launch_scan(
        self,
        query: str = "SOL",
    ) -> list[TokenMarketData]:

        return await self.launch.scan(
            query
        )

    async def scan_all(
        self,
        query: str = "SOL",
    ) -> dict[
        str,
        list[TokenMarketData]
    ]:

        market = await self.market_scan(
            query
        )

        launch = await self.launch_scan(
            query
        )

        return {
            "market": market,
            "launch": launch,
        }