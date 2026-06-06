class MigrationAI:

    @staticmethod
    def score(token):

        score = 0

        liquidity = token.get(
            "liquidity",
            0
        )

        volume = token.get(
            "volume",
            0
        )

        if volume > liquidity:
            score += 50

        if volume > liquidity * 2:
            score += 100

        if liquidity > 50000:
            score += 50

        return score