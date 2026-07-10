class CopyTradeConfidence:

    @staticmethod
    def calculate(wallet):

        confidence = 50

        confidence += min(
            wallet.get(
                "score",
                0
            ) / 20,
            25
        )

        confidence += min(
            wallet.get(
                "win_rate",
                0
            ) / 10,
            15
        )

        confidence += min(
            wallet.get(
                "roi",
                0
            ) / 20,
            10
        )

        return min(
            int(confidence),
            99
        )