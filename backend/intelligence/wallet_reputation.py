class WalletReputation:

    @staticmethod
    def reputation(wallet):

        score = wallet.get(
            "score",
            0
        )

        if score > 700:

            return 5

        if score > 500:

            return 4

        if score > 300:

            return 3

        if score > 150:

            return 2

        return 1