from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.storage.intelligence_repository import (
    IntelligenceRepository,
)


def make_result():

    token = TokenMarketData(
        symbol="TEST",
        address="TEST123",
        price_usd=1.25,
        liquidity_usd=50000,
        volume_24h_usd=100000,
        age_hours=1,
        source="test",
    )

    return IntelligenceResult(
        token=token,
        base_score=600,
        pattern_adjustment=150,
        launch_adjustment=100,
        migration_adjustment=0,
        final_score=850,
        confidence=75,
        pattern="BREAKOUT",
        risk="LOW",
        signal="STRONG",
    )


def test_result_to_record():

    result = make_result()

    record = (
        IntelligenceRepository.from_result(
            result
        )
    )

    assert (
        record.token_address
        == "TEST123"
    )

    assert (
        record.symbol
        == "TEST"
    )

    assert (
        record.score
        == 850
    )

    assert (
        record.confidence
        == 75
    )

    assert (
        record.pattern
        == "BREAKOUT"
    )

    assert (
        record.risk
        == "LOW"
    )

    assert (
        record.signal
        == "STRONG"
    )


def test_result_preserves_market_data():

    record = (
        IntelligenceRepository.from_result(
            make_result()
        )
    )

    assert record.price == 1.25

    assert record.liquidity == 50000

    assert record.volume == 100000


def test_record_serialization():

    record = (
        IntelligenceRepository.from_result(
            make_result()
        )
    )

    data = record.to_dict()

    assert (
        data["token_address"]
        == "TEST123"
    )

    assert (
        data["score"]
        == 850
    )

    assert (
        data["signal"]
        == "STRONG"
    )

    assert (
        "created_at"
        in data
    )


def test_multiple_results():

    first = make_result()

    second = make_result()

    records = (
        IntelligenceRepository.from_results(
            [
                first,
                second,
            ]
        )
    )

    assert len(records) == 2


def test_repository_serialization():

    records = (
        IntelligenceRepository.from_results(
            [
                make_result()
            ]
        )
    )

    data = (
        IntelligenceRepository.serialize(
            records
        )
    )

    assert len(data) == 1

    assert (
        data[0]["symbol"]
        == "TEST"
    )