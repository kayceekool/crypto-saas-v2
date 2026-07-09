class WalletLeaderboard:

    wallets = []

    @classmethod
    def update(
        cls,
        wallet
    ):

        cls.wallets.append(
            wallet
        )

        cls.wallets.sort(

            key=lambda w:

            w.get(
                "score",
                0
            ),

            reverse=True

        )

        cls.wallets = cls.wallets[:100]