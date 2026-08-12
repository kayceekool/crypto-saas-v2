from dataclasses import dataclass
from typing import Any

from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.services.intelligence_service import (
    IntelligenceService,
)

from backend.scanners.scanner_manager import (
    ScannerManager,
)


@dataclass
class ScanResult:

    market: list[IntelligenceResult]

    launch: list[IntelligenceResult]

    combined: list[IntelligenceResult]

    def to_dict(self) -> dict[str, Any]:

        return {
            "market": [
                item.to_dict()
                for item in self.market
            ],
            "launch": [
                item.to_dict()
                for item in self.launch
            ],
            "combined": [
                item.to_dict()
                for item in self.combined
            ],
        }


class ScanOrchestrator:

    def __init__(
        self,
        scanner_manager: ScannerManager,
        intelligence_service: (
            IntelligenceService | None
        ) = None,
    ):

        self.scanner = scanner_manager

        self.intelligence = (
            intelligence_service
            or IntelligenceService()
        )

    async def run(
        self,
        query: str = "SOL",
    ) -> ScanResult:

        scanner_results = (
            await self.scanner.scan_all(
                query
            )
        )

        market_tokens = (
            scanner_results.get(
                "market",
                [],
            )
        )

        launch_tokens = (
            scanner_results.get(
                "launch",
                [],
            )
        )

        market_results = (
            self.intelligence.rank(
                market_tokens
            )
        )

        launch_results = (
            self.intelligence.rank(
                launch_tokens
            )
        )

        combined_tokens = (
            market_tokens
            + launch_tokens
        )

        combined_results = (
            self.intelligence.rank(
                self._deduplicate_tokens(
                    combined_tokens
                )
            )
        )

        return ScanResult(
            market=market_results,
            launch=launch_results,
            combined=combined_results,
        )

    @staticmethod
    def _deduplicate_tokens(
        tokens,
    ):

        unique = {}

        for token in tokens:

            key = (
                token.address
                or
                token.pair_address
                or
                f"{token.source}:{token.symbol}"
            )

            if key not in unique:

                unique[key] = token

        return list(
            unique.values()
        )