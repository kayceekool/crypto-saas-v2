class CopyTradingEngine:

    tracked_wallets = {}

    @classmethod
    def add_wallet(
        cls,
        wallet
    ):

        cls.tracked_wallets[
            wallet
        ] = True

    @classmethod
    def wallets(cls):

        return list(
            cls.tracked_wallets.keys()
        )