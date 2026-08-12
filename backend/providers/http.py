from typing import Any

import httpx

from backend.providers.exceptions import (
    ProviderRequestError,
)


class ProviderHttpClient:

    def __init__(
        self,
        timeout: float = 20.0,
    ):

        self.timeout = timeout


    async def get_json(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:

        try:

            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    url,
                    params=params,
                    headers=headers,
                )

                response.raise_for_status()

                return response.json()

        except Exception as exc:

            raise ProviderRequestError(
                f"GET request failed: {url}"
            ) from exc


    async def post_json(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:

        try:

            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:

                response = await client.post(
                    url,
                    json=json,
                    headers=headers,
                )

                response.raise_for_status()

                return response.json()

        except Exception as exc:

            raise ProviderRequestError(
                f"POST request failed: {url}"
            ) from exc