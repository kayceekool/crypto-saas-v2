class LaunchAI:

    @staticmethod
    def score(token):

        score = 0

        age = token.get(
            "age_hours",
            999
        )

        liquidity = token.get(
            "liquidity",
            0
        )

        volume = token.get(
            "volume",
            0
        )

        if age < 1:
            score += 300

        elif age < 3:
            score += 200

        elif age < 6:
            score += 100

        if liquidity > 25000:
            score += 50

        if volume > liquidity:
            score += 100

        return score