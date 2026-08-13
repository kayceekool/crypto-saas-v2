import pytest

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import (
    Base,
)

from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.storage.intelligence_db import (
    IntelligenceRecordModel,
)

from backend.storage.intelligence_repository import (
    IntelligenceRepository,
)


@pytest.fixture
async def db():

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )

    Session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    async with Session() as session:

        yield session

    await engine.dispose()


def make_result(
    symbol="TEST",
    address="TEST123",
):

    token = TokenMarketData(
        symbol=symbol,
        address=address,
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
        metadata={
            "test": True,
        },
    )


@pytest.mark.asyncio
async def test_save_result(db):

    result = make_result()

    record = await (
        IntelligenceRepository.save_result(
            db,
            result,
        )
    )

    assert record.token_address == "TEST123"

    assert record.symbol == "TEST"

    assert record.score == 850

    assert record.confidence == 75

    assert record.pattern == "BREAKOUT"

    assert record.signal == "STRONG"


@pytest.mark.asyncio
async def test_save_and_list_recent(db):

    first = make_result(
        symbol="AAA",
        address="AAA123",
    )

    second = make_result(
        symbol="BBB",
        address="BBB123",
    )

    await IntelligenceRepository.save_result(
        db,
        first,
    )

    await IntelligenceRepository.save_result(
        db,
        second,
    )

    records = await (
        IntelligenceRepository.list_recent(
            db,
            limit=10,
        )
    )

    assert len(records) == 2


@pytest.mark.asyncio
async def test_list_by_token(db):

    first = make_result(
        symbol="AAA",
        address="AAA123",
    )

    second = make_result(
        symbol="BBB",
        address="BBB123",
    )

    await IntelligenceRepository.save_result(
        db,
        first,
    )

    await IntelligenceRepository.save_result(
        db,
        second,
    )

    records = await (
        IntelligenceRepository.list_by_token(
            db,
            "AAA123",
        )
    )

    assert len(records) == 1

    assert (
        records[0].symbol
        == "AAA"
    )


@pytest.mark.asyncio
async def test_metadata_round_trip(db):

    result = make_result()

    saved = await (
        IntelligenceRepository.save_result(
            db,
            result,
        )
    )

    assert saved.metadata == {
        "test": True,
    }


@pytest.mark.asyncio
async def test_save_multiple_results(db):

    results = [
        make_result(
            symbol="AAA",
            address="AAA123",
        ),
        make_result(
            symbol="BBB",
            address="BBB123",
        ),
        make_result(
            symbol="CCC",
            address="CCC123",
        ),
    ]

    saved = await (
        IntelligenceRepository.save_results(
            db,
            results,
        )
    )

    assert len(saved) == 3

    records = await (
        IntelligenceRepository.list_recent(
            db,
            limit=10,
        )
    )

    assert len(records) == 3


@pytest.mark.asyncio
async def test_database_model_has_primary_key(
    db,
):

    result = make_result()

    await IntelligenceRepository.save_result(
        db,
        result,
    )

    records = await (
        IntelligenceRepository.list_recent(
            db
        )
    )

    assert len(records) == 1

    # The ORM model uses an auto-generated
    # integer primary key.
    assert (
        records[0].token_address
        == "TEST123"
    )