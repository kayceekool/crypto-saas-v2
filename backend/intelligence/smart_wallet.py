class SmartWallet:

    @staticmethod
    def detect(wallet):

        return (

            wallet.get(
                "win_rate",
                0
            ) > 70

            and

            wallet.get(
                "roi",
                0
            ) > 30

        )