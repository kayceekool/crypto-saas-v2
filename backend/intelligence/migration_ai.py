class MigrationAI:

    @staticmethod
    def score(token):

        score = 0

        if token.get(
            "migrated",
            False
        ):
            score += 50

        if token.get(
            "raydium",
            False
        ):
            score += 100

        if token.get(
            "volume",
            0
        ) > 50000:
            score += 50

        return score