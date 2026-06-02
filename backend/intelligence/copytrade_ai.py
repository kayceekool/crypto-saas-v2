class CopyTradeAI:

    @staticmethod
    def generate_signal(
        wallet_rank,
        token_score
    ):

        if (
            wallet_rank == "ELITE"
            and token_score > 800
        ):

            return {
                "signal": "COPY_BUY",
                "confidence": 95
            }

        if (
            wallet_rank == "SMART"
            and token_score > 600
        ):

            return {
                "signal": "WATCH"
            }

        return None