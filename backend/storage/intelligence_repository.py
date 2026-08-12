from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.intelligence.persistence import (
    IntelligenceRecord,
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