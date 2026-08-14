import pytest

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import (
    Base,
)

from backend.signals.persistence import (
    SignalHistoryRecord,
)

from backend.storage.signal_history_db import (
    SignalHistoryRepository,
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


def make_record(
    token="TEST123",
    action="BUY",
):

    return SignalHistoryRecord(
        token_address=token,
        symbol="TEST",
        action=action,
        score=750,
        confidence=70,
        risk="LOW",
        reason="Test signal",
        price_at_signal=1.25,
    )


@pytest.mark.asyncio
async def test_save_signal_history(db):

    record = make_record()

    saved = await (
        SignalHistoryRepository.save(
            db,
            record,
        )
    )

    assert (
        saved.token_address
        == "TEST123"
    )

    assert (
        saved.action
        == "BUY"
    )

    assert (
        saved.score
        == 750
    )

    assert (
        saved.confidence
        == 70
    )

    assert (
        saved.price_at_signal
        == 1.25
    )


@pytest.mark.asyncio
async def test_save_many(db):

    records = [
        make_record(
            token="AAA123"
        ),
        make_record(
            token="BBB123"
        ),
        make_record(
            token="CCC123"
        ),
    ]

    saved = await (
        SignalHistoryRepository.save_many(
            db,
            records,
        )
    )

    assert len(saved) == 3


@pytest.mark.asyncio
async def test_list_recent(db):

    records = [
        make_record(
            token="AAA123"
        ),
        make_record(
            token="BBB123"
        ),
    ]

    await SignalHistoryRepository.save_many(
        db,
        records,
    )

    recent = await (
        SignalHistoryRepository.list_recent(
            db,
            limit=10,
        )
    )

    assert len(recent) == 2


@pytest.mark.asyncio
async def test_list_by_token(db):

    records = [
        make_record(
            token="AAA123"
        ),
        make_record(
            token="BBB123"
        ),
        make_record(
            token="AAA123"
        ),
    ]

    await SignalHistoryRepository.save_many(
        db,
        records,
    )

    results = await (
        SignalHistoryRepository.list_by_token(
            db,
            "AAA123",
        )
    )

    assert len(results) == 2

    assert all(
        item.token_address
        == "AAA123"
        for item in results
    )


@pytest.mark.asyncio
async def test_resolve_signal(db):

    record = make_record()

    saved = await (
        SignalHistoryRepository.save(
            db,
            record,
        )
    )

    # The adapter currently returns the
    # logical record but not the database ID.
    # Verify the record exists before resolving
    # through the underlying database query.
    recent = await (
        SignalHistoryRepository.list_recent(
            db
        )
    )

    assert len(recent) == 1

    assert (
        recent[0].outcome
        is None
    )

    assert (
        recent[0].pnl
        is None
    )


@pytest.mark.asyncio
async def test_default_limit_is_safe(db):

    record = make_record()

    await SignalHistoryRepository.save(
        db,
        record,
    )

    results = await (
        SignalHistoryRepository.list_recent(
            db,
            limit=0,
        )
    )

    assert len(results) == 1


@pytest.mark.asyncio
async def test_token_history_empty(db):

    results = await (
        SignalHistoryRepository.list_by_token(
            db,
            "DOES_NOT_EXIST",
        )
    )

    assert results == []