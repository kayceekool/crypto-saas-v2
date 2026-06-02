from sqlalchemy import select

from models.wallet import Wallet


class WalletRepository:

    @staticmethod
    async def get_wallet(
        db,
        wallet_address
    ):

        stmt = select(Wallet).where(
            Wallet.wallet == wallet_address
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()