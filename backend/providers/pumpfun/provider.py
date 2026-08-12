from backend.core.logging import (
    get_logger,
)

from backend.core.settings import (
    settings,
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
    "provider.pumpfun"
)


class PumpFunProvider(
    BaseProvider
):

    name = "pumpfun"


    def __init__(
        self,
        client: ProviderHttpClient | None = None,
        base_url: str | None = None,
    ):

        self.client = (
            client
            or
            ProviderHttpClient()
        )

        self.base_url = (
            base_url
            or
            getattr(
                settings,
                "pumpfun_api_url",
                "",
            )
        )


    async def search(
        self,
        query: str,
    ) -> list[TokenMarketData]:

        if not self.base_url:

            logger.warning(
                "Pump.fun provider URL "
                "is not configured."
            )

            return []

        payload = await self.client.get_json(
            self.base_url,
            params={
                "q": query,
            },
        )

        if not isinstance(
            payload,
            list,
        ):

            if isinstance(
                payload,
                dict,
            ):

                payload = payload.get(
                    "data",
                    []
                )

            else:

                payload = []

        results = []

        for item in payload:

            if not isinstance(
                item,
                dict,
            ):
                continue

            results.append(
                TokenMarketData(
                    symbol=item.get(
                        "symbol",
                        item.get(
                            "name",
                            "UNKNOWN",
                        ),
                    ),
                    address=item.get(
                        "mint",
                        item.get(
                            "address",
                            "",
                        ),
                    ),
                    chain="solana",
                    source=self.name,
                    metadata=item,
                )
            )

        return results


    async def health_check(self) -> bool:

        if not self.base_url:

            return False

        try:

            await self.search("")

            return True

        except Exception:

            logger.exception(
                "Pump.fun health check failed."
            )

            return False