from typing import Any

from backend.core.logging import (
    get_logger,
)

from backend.core.settings import (
    settings,
)

from backend.providers.base import (
    BaseProvider,
)

from backend.providers.exceptions import (
    ProviderConfigurationError,
)

from backend.providers.http import (
    ProviderHttpClient,
)


logger = get_logger(
    "provider.helius"
)


class HeliusProvider(
    BaseProvider
):

    name = "helius"


    def __init__(
        self,
        client: ProviderHttpClient | None = None,
        api_key: str | None = None,
        rpc_url: str | None = None,
    ):

        self.client = (
            client
            or
            ProviderHttpClient()
        )

        self.api_key = (
            api_key
            or
            getattr(
                settings,
                "helius_api_key",
                "",
            )
        )

        self.rpc_url = (
            rpc_url
            or
            getattr(
                settings,
                "helius_rpc_url",
                "",
            )
        )


    def _validate(
        self,
    ) -> None:

        if not self.api_key:

            raise ProviderConfigurationError(
                "HELIUS_API_KEY is not configured."
            )

        if not self.rpc_url:

            raise ProviderConfigurationError(
                "HELIUS_RPC_URL is not configured."
            )


    async def rpc(
        self,
        method: str,
        params: list[Any] | None = None,
    ) -> Any:

        self._validate()

        payload = {

            "jsonrpc": "2.0",

            "id": 1,

            "method": method,

            "params": params or [],
        }

        return await self.client.post_json(
            self.rpc_url,
            json=payload,
        )


    async def search(
        self,
        query: str,
    ):

        """
        Helius is not treated as a market-search
        provider in Package 02.

        Token discovery remains the responsibility
        of market-data providers such as DexScreener
        and Pump.fun.
        """

        return []


    async def health_check(self) -> bool:

        try:

            await self.rpc(
                "getHealth"
            )

            return True

        except Exception:

            logger.exception(
                "Helius health check failed."
            )

            return False