from backend.providers.models import (
    TokenMarketData,
)


class ScoringEngine:

    @staticmethod
    def calculate(
        token: TokenMarketData,
    ) -> float:

        score = 0.0

        liquidity = max(
            token.liquidity_usd,
            0.0,
        )

        volume = max(
            token.volume_24h_usd,
            0.0,
        )

        age = token.age_hours

        score += min(
            liquidity / 1000.0,
            250.0,
        )

        score += min(
            volume / 1000.0,
            350.0,
        )

        if age < 1:

            score += 500.0

        elif age < 3:

            score += 250.0

        elif age < 12:

            score += 100.0

        return round(
            score,
            2,
        )