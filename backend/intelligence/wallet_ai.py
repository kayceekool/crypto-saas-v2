class WalletAI:

    @staticmethod
    def calculate(wallet):

        score = 0

        roi = wallet.get("roi", 0)

        win_rate = wallet.get("win_rate", 0)

        trades = wallet.get("total_trades", 0)

        if roi > 100:
            score += 300

        elif roi > 50:
            score += 200

        elif roi > 20:
            score += 100

        if win_rate > 80:
            score += 300

        elif win_rate > 70:
            score += 200

        elif win_rate > 60:
            score += 100

        score += min(trades, 300)

        return score