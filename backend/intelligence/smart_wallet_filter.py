from core.config import (
    SMART_WALLET_MIN_WINRATE
)


class SmartWalletFilter:

    @staticmethod
    def qualifies(
        wallet
    ):

        return (
            wallet.win_rate
            >= SMART_WALLET_MIN_WINRATE
        )