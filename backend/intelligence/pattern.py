from backend.providers.models import (
    TokenMarketData,
)


class PatternAI:

    @staticmethod
    def detect(
        token: TokenMarketData,
        score: float,
    ) -> tuple[str, float]:

        volume = max(
            token.volume_24h_usd,
            0.0,
        )

        liquidity = max(
            token.liquidity_usd,
            0.0,
        )

        if (
            score > 800
            and liquidity > 0
            and volume > liquidity * 3
        ):

            return (
                "BREAKOUT",
                150.0,
            )

        if (
            score > 500
            and liquidity > 0
            and volume > liquidity
        ):

            return (
                "ACCUMULATION",
                75.0,
            )

        return (
            "NORMAL",
            0.0,
        )