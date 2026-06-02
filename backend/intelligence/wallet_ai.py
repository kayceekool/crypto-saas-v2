class WalletAI:

    @staticmethod
    def calculate_score(wallet):

        score = 0

        score += wallet.win_rate * 3

        score += wallet.roi

        score += (
            wallet.total_trades * 0.2
        )

        return round(score, 2)