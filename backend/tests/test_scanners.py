import pytest

from backend.core.provider_registry import (
    ProviderRegistry,
)

from backend.providers.base import (
    BaseProvider,
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

from backend.scanners.scanner_manager import (
    ScannerManager,
)


class FakeMarketProvider(
    BaseProvider
):

    name = "fake-market"

    def __init__(
        self,
        tokens=None,
    ):

        self.tokens = tokens or []

    async def search(
        self,
        query: str,
    ):

        return self.tokens


class FakePumpFunProvider(
    BaseProvider
):

    name = "pumpfun"

    def __init__(
        self,
        tokens=None,
    ):

        self.tokens = tokens or []

    async def search(
        self,
        query: str,
    ):

        return self.tokens


@pytest.mark.asyncio
async def test_market_scanner():

    tokens = [

        TokenMarketData(
            symbol="SOL",
            address="SOL123",
            source="fake-market",
        ),

        TokenMarketData(
            symbol="BONK",
            address="BONK123",
            source="fake-market",
        ),
    ]

    registry = ProviderRegistry()

    registry.register(
        "fake-market",
        FakeMarketProvider(
            tokens
        ),
    )

    scanner = MarketScanner(
        registry
    )

    results = await scanner.scan(
        "SOL"
    )

    assert len(results) == 2

    assert (
        results[0].symbol
        == "SOL"
    )


@pytest.mark.asyncio
async def test_market_scanner_deduplicates():

    token = TokenMarketData(
        symbol="TEST",
        address="SAME_ADDRESS",
        source="fake",
    )

    provider_a = FakeMarketProvider(
        [token]
    )

    provider_b = FakeMarketProvider(
        [token]
    )

    registry = ProviderRegistry()

    registry.register(
        "provider-a",
        provider_a,
        priority=10,
    )

    registry.register(
        "provider-b",
        provider_b,
        priority=20,
    )

    scanner = MarketScanner(
        registry
    )

    results = await scanner.scan(
        "TEST"
    )

    assert len(results) == 1


@pytest.mark.asyncio
async def test_launch_scanner_filters_recent_tokens():

    recent = TokenMarketData(
        symbol="NEW",
        address="NEW123",
        age_hours=0.5,
        source="pumpfun",
    )

    old = TokenMarketData(
        symbol="OLD",
        address="OLD123",
        age_hours=5,
        source="pumpfun",
    )

    registry = ProviderRegistry()

    registry.register(
        "pumpfun",
        FakePumpFunProvider(
            [
                recent,
                old,
            ]
        ),
    )

    scanner = LaunchScanner(
        registry
    )

    results = await scanner.scan(
        "SOL"
    )

    assert len(results) == 1

    assert (
        results[0].symbol
        == "NEW"
    )


@pytest.mark.asyncio
async def test_scanner_manager():

    token = TokenMarketData(
        symbol="TEST",
        address="TEST123",
        source="fake-market",
    )

    registry = ProviderRegistry()

    registry.register(
        "fake-market",
        FakeMarketProvider(
            [token]
        ),
    )

    registry.register(
        "pumpfun",
        FakePumpFunProvider(
            []
        ),
    )

    manager = ScannerManager(
        registry
    )

    results = await manager.scan_all(
        "TEST"
    )

    assert "market" in results

    assert "launch" in results

    assert len(
        results["market"]
    ) == 1

    assert len(
        results["launch"]
    ) == 0