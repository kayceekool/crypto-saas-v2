from abc import ABC, abstractmethod

from backend.providers.models import (
    TokenMarketData,
)


class BaseScanner(ABC):

    name = "base"

    @abstractmethod
    async def scan(
        self,
        query: str,
    ) -> list[TokenMarketData]:

        raise NotImplementedError