from backend.providers.models import (
    TokenMarketData,
)


class MigrationAI:

    @staticmethod
    def score(
        token: TokenMarketData,
    ) -> float:

        adjustment = 0.0

        metadata = token.metadata or {}

        migrated = bool(
            metadata.get(
                "migrated",
                False,
            )
        )

        raydium = bool(
            metadata.get(
                "raydium",
                False,
            )
        )

        if migrated:

            adjustment += 50.0

        if raydium:

            adjustment += 100.0

        if token.volume_24h_usd > 50000:

            adjustment += 50.0

        return adjustment