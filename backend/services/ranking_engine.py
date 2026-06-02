class RankingEngine:

    @staticmethod
    def rank(tokens):

        return sorted(
            tokens,
            key=lambda x: x["score"],
            reverse=True
        )