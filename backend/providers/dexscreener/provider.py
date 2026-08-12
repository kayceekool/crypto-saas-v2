from backend.core.logging import (
    get_logger,
)

from backend.providers.base import (
    BaseProvider,
)

from backend.providers.http import (
    ProviderHttpClient,
)

from backend.providers.models import (
    TokenMarketData,
)


logger = get_logger(
    "provider.dexscreener"
)


class DexScreenerProvider(
    BaseProvider
):

    name = "dexscreener"

    BASE_URL = (
        "https://api.dexscreener.com"
    )

    SEARCH_PATH = "/latest/dex/search"


    def __init__(
        self,
        client: ProviderHttpClient | None = None,
    ):

        self.client = (
            client
            or
            ProviderHttpClient()
        )


    async def search(
        self,
        query: str,
    ) -> list[TokenMarketData]:

        payload = await self.client.get_json(
            f"{self.BASE_URL}"
            f"{self.SEARCH_PATH}",
            params={
                "q": query,
            },
        )

        pairs = payload.get(
            "pairs",
            [],
        )

        results = []

        for pair in pairs:

            if not isinstance(
                pair,
                dict,
            ):
                continue

            chain = pair.get(
                "chainId",
                "unknown",
            )

            if chain != "solana":
                continue

            base_token = pair.get(
                "baseToken",
                {},
            )

            liquidity = pair.get(
                "liquidity",
                {},
            )

            volume = pair.get(
                "volume",
                {},
            )

            market_cap = (
                pair.get(
                    "marketCap",
                    0,
                )
                or
                0
            )

            try:

                price = float(
                    pair.get(
                        "priceUsd",
                        0,
                    )
                    or
                    0
                )

            except (
                TypeError,
                ValueError,
            ):

                price = 0.0

            try:

                liquidity_usd = float(
                    liquidity.get(
                        "usd",
                        0,
                    )
                    or
                    0
                )

            except (
                TypeError,
                ValueError,
            ):

                liquidity_usd = 0.0

            try:

                volume_24h = float(
                    volume.get(
                        "h24",
                        0,
                    )
                    or
                    0
                )

            except (
                TypeError,
                ValueError,
            ):

                volume_24h = 0.0

            try:

                market_cap_usd = float(
                    market_cap
                )

            except (
                TypeError,
                ValueError,
            ):

                market_cap_usd = 0.0

            results.append(
                TokenMarketData(
                    symbol=base_token.get(
                        "symbol",
                        "UNKNOWN",
                    ),
                    address=base_token.get(
                        "address",
                        "",
                    ),
                    chain="solana",
                    price_usd=price,
                    liquidity_usd=(
                        liquidity_usd
                    ),
                    volume_24h_usd=(
                        volume_24h
                    ),
                    market_cap_usd=(
                        market_cap_usd
                    ),
                    pair_address=pair.get(
                        "pairAddress",
                        "",
                    ),
                    source=self.name,
                    metadata={
                        "dexId":
                            pair.get(
                                "dexId"
                            ),
                        "url":
                            pair.get(
                                "url"
                            ),
                    },
                )
            )

        logger.info(
            "DexScreener returned %d "
            "Solana pair(s).",
            len(results),
        )

        return results


    async def health_check(self) -> bool:

        try:

            await self.search("SOL")

            return True

        except Exception:

            logger.exception(
                "DexScreener health check failed."
            )

            return False