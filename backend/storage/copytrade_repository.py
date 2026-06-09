from models.copytrade_signal import (
    CopyTradeSignal
)


class CopyTradeRepository:

    @staticmethod
    async def save_signal(
        db,
        wallet,
        token,
        action,
        confidence
    ):

        signal = CopyTradeSignal(
            wallet=wallet,
            token=token,
            action=action,
            confidence=confidence
        )

        db.add(
            signal
        )

        await db.commit()

        return signal