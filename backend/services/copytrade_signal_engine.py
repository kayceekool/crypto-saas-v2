from intelligence.copytrade_selector import (
    CopyTradeSelector
)

from intelligence.copytrade_confidence import (
    CopyTradeConfidence
)


class CopyTradeSignalEngine:

    @staticmethod
    def build(wallet, trade):

        if not CopyTradeSelector.should_follow(
            wallet
        ):
            return None

        return {

            "wallet":
                wallet["wallet"],

            "token":
                trade["token"],

            "action":
                trade["action"],

            "price":
                trade.get(
                    "price",
                    0
                ),

            "confidence":
                CopyTradeConfidence.calculate(
                    wallet
                )
        }