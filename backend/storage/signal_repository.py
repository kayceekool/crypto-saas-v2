from models.signal_history import (
    SignalHistory
)


class SignalRepository:

    @staticmethod
    async def save_signal(
        db,
        signal_data
    ):

        record = SignalHistory(
            token=signal_data["token"],
            signal=signal_data["signal"],
            score=signal_data["score"],
            confidence=signal_data["confidence"],
            price_at_signal=signal_data["price"]
        )

        db.add(record)

        await db.commit()