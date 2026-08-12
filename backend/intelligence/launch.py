from backend.providers.models import (
    TokenMarketData,
)


class LaunchAI:

    @staticmethod
    def score(
        token: TokenMarketData,
    ) -> float:

        adjustment = 0.0

        age = token.age_hours

        if age < 1:

            adjustment += 150.0

        elif age < 3:

            adjustment += 100.0

        elif age < 6:

            adjustment += 50.0

        if token.liquidity_usd > 25000:

            adjustment += 50.0

        return adjustment