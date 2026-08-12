from abc import ABC, abstractmethod

from backend.providers.models import (
    TokenMarketData,
)


class BaseProvider(ABC):

    name = "base"

    @abstractmethod
    async def search(
        self,
        query: str,
    ) -> list[TokenMarketData]:

        raise NotImplementedError


    async def health_check(self) -> bool:

        return True