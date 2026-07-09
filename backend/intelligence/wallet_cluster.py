class WalletCluster:

    clusters = {}

    @classmethod
    def update(
        cls,
        wallet,
        token
    ):

        if token not in cls.clusters:

            cls.clusters[token] = []

        cls.clusters[token].append(
            wallet
        )

    @classmethod
    def size(
        cls,
        token
    ):

        return len(

            cls.clusters.get(
                token,
                []
            )

        )