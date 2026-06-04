class PatternAI:

    @staticmethod
    def detect(token):

        score = token.get("score", 0)

        volume = token.get("volume", 0)

        liquidity = token.get("liquidity", 0)

        if (
            score > 800 and
            volume > liquidity * 3
        ):
            return "BREAKOUT"

        if (
            score > 500 and
            volume > liquidity
        ):
            return "ACCUMULATION"

        return "NORMAL"