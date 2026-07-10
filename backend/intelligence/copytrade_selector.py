class CopyTradeSelector:

    @staticmethod
    def should_follow(wallet):

        return (

            wallet.get(
                "smart_wallet",
                False
            )

            and

            wallet.get(
                "score",
                0
            ) >= 600

            and

            wallet.get(
                "win_rate",
                0
            ) >= 70

        )