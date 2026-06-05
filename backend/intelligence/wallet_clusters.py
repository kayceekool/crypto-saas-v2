class WalletClusters:

    @staticmethod
    def cluster(wallets):

        clusters = {}

        for wallet in wallets:

            category = "NORMAL"

            if wallet.get(
                "win_rate",
                0
            ) > 70:

                category = "ELITE"

            elif wallet.get(
                "win_rate",
                0
            ) > 55:

                category = "SMART"

            clusters.setdefault(
                category,
                []
            ).append(wallet)

        return clusters