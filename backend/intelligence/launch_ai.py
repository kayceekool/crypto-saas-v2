class LaunchAI:

    @staticmethod
    def score(token):

        score = 0

        age = token.get(
            "age_hours",
            999
        )

        if age < 1:
            score += 150

        elif age < 3:
            score += 100

        elif age < 6:
            score += 50

        if token.get(
            "liquidity",
            0
        ) > 25000:
            score += 50

        return score