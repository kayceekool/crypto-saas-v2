import pytest

from backend.providers.base import (
    BaseProvider,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.providers.http import (
    ProviderHttpClient,
)

from backend.providers.dexscreener.provider import (
    DexScreenerProvider,
)

from backend.providers.pumpfun.provider import (
    PumpFunProvider,
)

from backend.providers.helius.provider import (
    HeliusProvider,
)


class FakeProvider(
    BaseProvider
):

    name = "fake"

    async def search(
        self,
        query: str,
    ):

        return [
            TokenMarketData(
                symbol="TEST",
                address="ABC",
                source=self.name,
            )
        ]


@pytest.mark.asyncio
async def test_base_provider_contract():

    provider = FakeProvider()

    results = await provider.search(
        "test"
    )

    assert len(results) == 1

    assert (
        results[0].symbol
        == "TEST"
    )

    assert (
        results[0].source
        == "fake"
    )


def test_token_market_data():

    token = TokenMarketData(
        symbol="SOL",
        address="123",
        price_usd=100.0,
        liquidity_usd=50000.0,
        volume_24h_usd=100000.0,
        source="test",
    )

    data = token.to_dict()

    assert data["symbol"] == "SOL"

    assert (
        data["price_usd"]
        == 100.0
    )

    assert (
        data["liquidity_usd"]
        == 50000.0
    )


def test_dexscreener_provider():

    provider = DexScreenerProvider(
        client=ProviderHttpClient()
    )

    assert (
        provider.name
        == "dexscreener"
    )


def test_pumpfun_provider():

    provider = PumpFunProvider(
        client=ProviderHttpClient()
    )

    assert (
        provider.name
        == "pumpfun"
    )


def test_helius_provider():

    provider = HeliusProvider(
        client=ProviderHttpClient()
    )

    assert (
        provider.name
        == "helius"
    )