class PatternAI:

    @staticmethod
    def detect(token):

        score = token.get("score", 0)

        volume = token.get("volume", 0)

        liquidity = token.get("liquidity", 0)

        age = token.get(
            "age_hours",
            999
        )

        if (
            age < 6 and
            volume > liquidity * 1.5
        ):
            return "BREAKOUT"

        if (
            volume > liquidity * 0.75
        ):
            return "ACCUMULATION"

        return "NORMAL"