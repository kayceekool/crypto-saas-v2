from intelligence.wallet_ai import WalletAI
from intelligence.wallet_rank import WalletRank
from intelligence.smart_wallet import SmartWallet
from intelligence.whale_detector import WhaleDetector
from intelligence.wallet_reputation import WalletReputation


class WalletIntelligence:

    @staticmethod
    def enhance(wallet):

        wallet["score"] = WalletAI.calculate(
            wallet
        )

        wallet["rank"] = WalletRank.rank(
            wallet["score"]
        )

        wallet["smart_wallet"] = SmartWallet.detect(
            wallet
        )

        wallet["whale"] = WhaleDetector.detect(
            wallet
        )

        wallet["reputation"] = WalletReputation.reputation(
            wallet
        )

        return wallet