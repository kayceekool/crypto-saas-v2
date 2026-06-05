class SmartMoneyAI:

    MIN_WALLET_SCORE = 75

    @staticmethod
    def evaluate(wallet):

        score = 0

        if wallet.get("win_rate", 0) > 60:
            score += 25

        if wallet.get("profit_usd", 0) > 10000:
            score += 25

        if wallet.get("successful_trades", 0) > 20:
            score += 25

        if wallet.get("avg_roi", 0) > 30:
            score += 25

        return {
            "wallet": wallet.get("address"),
            "score": score,
            "smart_money": (
                score >=
                SmartMoneyAI.MIN_WALLET_SCORE
            )
        }