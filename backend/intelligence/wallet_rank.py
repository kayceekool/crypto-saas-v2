class WalletRank:

    @staticmethod
    def rank(score):

        if score >= 800:
            return "LEGEND"

        if score >= 600:
            return "ELITE"

        if score >= 450:
            return "SMART"

        if score >= 300:
            return "GOOD"

        return "NORMAL"