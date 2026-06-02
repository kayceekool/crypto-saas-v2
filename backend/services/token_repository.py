from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Token


class TokenRepository:

    @staticmethod
    async def save_token(
        db: AsyncSession,
        token_data: dict
    ):

        stmt = select(Token).where(
            Token.address == token_data["address"]
        )

        result = await db.execute(stmt)

        existing = result.scalar_one_or_none()

        if existing:

            existing.price = token_data["price"]
            existing.volume = token_data["volume"]
            existing.liquidity = token_data["liquidity"]
            existing.market_cap = token_data["market_cap"]
            existing.score = token_data["score"]

        else:

            db.add(
                Token(
                    symbol=token_data["symbol"],
                    address=token_data["address"],
                    price=token_data["price"],
                    volume=token_data["volume"],
                    liquidity=token_data["liquidity"],
                    market_cap=token_data["market_cap"],
                    score=token_data["score"]
                )
            )

        await db.commit()