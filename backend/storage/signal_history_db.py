import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.Signal_history import (
    SignalHistory,
)

from backend.signals.persistence import (
    SignalHistoryRecord,
)


class SignalHistoryRepository:

    @staticmethod
    def _to_model(
        record: SignalHistoryRecord,
    ) -> SignalHistory:

        return SignalHistory(
            token=record.token_address,
            signal=record.action,
            score=record.score,
            confidence=record.confidence,
            price_at_signal=(
                record.price_at_signal
            ),
            outcome=record.outcome,
            pnl=record.pnl,
            created_at=record.created_at,
        )

    @staticmethod
    def _from_model(
        model: SignalHistory,
    ) -> SignalHistoryRecord:

        return SignalHistoryRecord(
            token_address=model.token,
            symbol=model.token,
            action=model.signal,
            score=model.score,
            confidence=model.confidence,
            risk="UNKNOWN",
            reason="",
            price_at_signal=(
                model.price_at_signal or 0.0
            ),
            outcome=model.outcome,
            pnl=model.pnl,
            created_at=model.created_at,
        )

    @classmethod
    async def save(
        cls,
        db: AsyncSession,
        record: SignalHistoryRecord,
    ) -> SignalHistoryRecord:

        model = cls._to_model(
            record
        )

        db.add(model)

        await db.commit()

        await db.refresh(model)

        return cls._from_model(
            model
        )

    @classmethod
    async def save_many(
        cls,
        db: AsyncSession,
        records: list[
            SignalHistoryRecord
        ],
    ) -> list[
        SignalHistoryRecord
    ]:

        models = [
            cls._to_model(record)
            for record in records
        ]

        db.add_all(models)

        await db.commit()

        for model in models:

            await db.refresh(model)

        return [
            cls._from_model(model)
            for model in models
        ]

    @classmethod
    async def list_recent(
        cls,
        db: AsyncSession,
        limit: int = 100,
    ) -> list[
        SignalHistoryRecord
    ]:

        safe_limit = max(
            1,
            min(limit, 1000),
        )

        stmt = (
            select(SignalHistory)
            .order_by(
                SignalHistory.created_at.desc()
            )
            .limit(safe_limit)
        )

        result = await db.execute(stmt)

        models = result.scalars().all()

        return [
            cls._from_model(model)
            for model in models
        ]

    @classmethod
    async def list_by_token(
        cls,
        db: AsyncSession,
        token_address: str,
        limit: int = 100,
    ) -> list[
        SignalHistoryRecord
    ]:

        safe_limit = max(
            1,
            min(limit, 1000),
        )

        stmt = (
            select(SignalHistory)
            .where(
                SignalHistory.token
                == token_address
            )
            .order_by(
                SignalHistory.created_at.desc()
            )
            .limit(safe_limit)
        )

        result = await db.execute(stmt)

        models = result.scalars().all()

        return [
            cls._from_model(model)
            for model in models
        ]

    @classmethod
    async def resolve(
        cls,
        db: AsyncSession,
        record_id: int,
        outcome: str,
        pnl: float,
    ) -> SignalHistoryRecord | None:

        stmt = (
            select(SignalHistory)
            .where(
                SignalHistory.id
                == record_id
            )
        )

        result = await db.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:

            return None

        model.outcome = outcome

        model.pnl = float(pnl)

        await db.commit()

        await db.refresh(model)

        return cls._from_model(
            model
        )