class ScoringEngine:

    @staticmethod
    def calculate(token):

        score = 0

        liquidity = token.get("liquidity", 0)
        volume = token.get("volume", 0)
        age = token.get("age_hours", 999)

        score += min(liquidity / 1000, 250)

        score += min(volume / 1000, 350)

        if age < 1:
            score += 500

        elif age < 3:
            score += 250

        elif age < 12:
            score += 100

        return int(score)