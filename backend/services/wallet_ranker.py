class WalletRanker:

    @staticmethod
    def rank(wallet):

        if wallet.score >= 300:
            return "ELITE"

        if wallet.score >= 200:
            return "SMART"

        if wallet.score >= 100:
            return "GOOD"

        return "NORMAL"