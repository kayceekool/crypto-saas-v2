from sqlalchemy import select

from models.token import (
    Token
)


class TokenRepository:

    @staticmethod
    async def save_token(
        db,
        token_data
    ):

        stmt = select(Token).where(
            Token.address ==
            token_data["address"]
        )

        result = await db.execute(
            stmt
        )

        existing = (
            result.scalar_one_or_none()
        )

        if existing:

            existing.price = (
                token_data.get(
                    "price",
                    0
                )
            )

            existing.liquidity = (
                token_data.get(
                    "liquidity",
                    0
                )
            )

            existing.volume = (
                token_data.get(
                    "volume",
                    0
                )
            )

            existing.score = (
                token_data.get(
                    "score",
                    0
                )
            )

            existing.signal = (
                token_data.get(
                    "signal",
                    ""
                )
            )

            existing.rating = (
                token_data.get(
                    "rating",
                    ""
                )
            )

        else:

            existing = Token(
                **token_data
            )

            db.add(
                existing
            )

        await db.commit()

        return existing