import json

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.intelligence.persistence import (
    IntelligenceRecord,
)

from backend.storage.intelligence_db import (
    IntelligenceRecordModel,
)


class IntelligenceRepository:

    @staticmethod
    def from_result(
        result: IntelligenceResult,
    ) -> IntelligenceRecord:

        token = result.token

        return IntelligenceRecord(
            token_address=(
                token.address
            ),
            symbol=(
                token.symbol
            ),
            score=(
                result.final_score
            ),
            confidence=(
                result.confidence
            ),
            pattern=(
                result.pattern
            ),
            risk=(
                result.risk
            ),
            signal=(
                result.signal
            ),
            price=(
                token.price_usd
            ),
            liquidity=(
                token.liquidity_usd
            ),
            volume=(
                token.volume_24h_usd
            ),
            metadata=(
                result.metadata.copy()
            ),
        )

    @classmethod
    def from_results(
        cls,
        results: list[
            IntelligenceResult
        ],
    ) -> list[
        IntelligenceRecord
    ]:

        return [
            cls.from_result(
                result
            )
            for result in results
        ]

    @staticmethod
    def serialize(
        records: list[
            IntelligenceRecord
        ],
    ) -> list[dict]:

        return [
            record.to_dict()
            for record in records
        ]

    @staticmethod
    def _to_model(
        record: IntelligenceRecord,
    ) -> IntelligenceRecordModel:

        return IntelligenceRecordModel(
            token_address=(
                record.token_address
            ),
            symbol=(
                record.symbol
            ),
            score=(
                record.score
            ),
            confidence=(
                record.confidence
            ),
            pattern=(
                record.pattern
            ),
            risk=(
                record.risk
            ),
            signal=(
                record.signal
            ),
            price=(
                record.price
            ),
            liquidity=(
                record.liquidity
            ),
            volume=(
                record.volume
            ),
            metadata_json=json.dumps(
                record.metadata or {}
            ),
            created_at=(
                record.created_at
            ),
        )

    @staticmethod
    def _from_model(
        model: IntelligenceRecordModel,
    ) -> IntelligenceRecord:

        metadata = {}

        if model.metadata_json:

            try:

                metadata = json.loads(
                    model.metadata_json
                )

            except json.JSONDecodeError:

                metadata = {}

        return IntelligenceRecord(
            token_address=(
                model.token_address
            ),
            symbol=(
                model.symbol
            ),
            score=(
                model.score
            ),
            confidence=(
                model.confidence
            ),
            pattern=(
                model.pattern
            ),
            risk=(
                model.risk
            ),
            signal=(
                model.signal
            ),
            price=(
                model.price
            ),
            liquidity=(
                model.liquidity
            ),
            volume=(
                model.volume
            ),
            created_at=(
                model.created_at
            ),
            metadata=metadata,
        )

    @classmethod
    async def save(
        cls,
        db: AsyncSession,
        record: IntelligenceRecord,
    ) -> IntelligenceRecord:

        model = cls._to_model(
            record
        )

        db.add(model)

        await db.commit()

        await db.refresh(
            model
        )

        return cls._from_model(
            model
        )

    @classmethod
    async def save_result(
        cls,
        db: AsyncSession,
        result: IntelligenceResult,
    ) -> IntelligenceRecord:

        record = cls.from_result(
            result
        )

        return await cls.save(
            db,
            record,
        )

    @classmethod
    async def save_results(
        cls,
        db: AsyncSession,
        results: list[
            IntelligenceResult
        ],
    ) -> list[
        IntelligenceRecord
    ]:

        records = cls.from_results(
            results
        )

        models = [
            cls._to_model(
                record
            )
            for record in records
        ]

        db.add_all(
            models
        )

        await db.commit()

        for model in models:

            await db.refresh(
                model
            )

        return [
            cls._from_model(
                model
            )
            for model in models
        ]

    @classmethod
    async def list_recent(
        cls,
        db: AsyncSession,
        limit: int = 100,
    ) -> list[
        IntelligenceRecord
    ]:

        safe_limit = max(
            1,
            min(
                limit,
                1000,
            ),
        )

        stmt = (
            select(
                IntelligenceRecordModel
            )
            .order_by(
                IntelligenceRecordModel.created_at.desc()
            )
            .limit(
                safe_limit
            )
        )

        result = await db.execute(
            stmt
        )

        models = result.scalars().all()

        return [
            cls._from_model(
                model
            )
            for model in models
        ]

    @classmethod
    async def list_by_token(
        cls,
        db: AsyncSession,
        token_address: str,
        limit: int = 100,
    ) -> list[
        IntelligenceRecord
    ]:

        safe_limit = max(
            1,
            min(
                limit,
                1000,
            ),
        )

        stmt = (
            select(
                IntelligenceRecordModel
            )
            .where(
                IntelligenceRecordModel.token_address
                == token_address
            )
            .order_by(
                IntelligenceRecordModel.created_at.desc()
            )
            .limit(
                safe_limit
            )
        )

        result = await db.execute(
            stmt
        )

        models = result.scalars().all()

        return [
            cls._from_model(
                model
            )
            for model in models
        ]