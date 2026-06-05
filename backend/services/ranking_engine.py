class RankingEngine:

    @staticmethod
    def rank(tokens):

        return sorted(
            tokens,
            key=lambda t:
                t.get(
                    "score",
                    0
                ),
            reverse=True
        )