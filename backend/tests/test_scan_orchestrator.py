import pytest

from backend.intelligence.models import (
    IntelligenceResult,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.services.scan_orchestrator import (
    ScanOrchestrator,
)


class FakeScanner:

    def __init__(
        self,
        market=None,
        launch=None,
    ):

        self.market = market or []

        self.launch = launch or []

    async def scan_all(
        self,
        query,
    ):

        return {
            "market": self.market,
            "launch": self.launch,
        }


class FakeIntelligence:

    def rank(
        self,
        tokens,
    ):

        results = []

        for token in tokens:

            results.append(
                IntelligenceResult(
                    token=token,
                    base_score=100,
                    final_score=100,
                    confidence=60,
                    pattern="NORMAL",
                    risk="LOW",
                    signal="WATCH",
                )
            )

        return sorted(
            results,
            key=lambda item:
                item.final_score,
            reverse=True,
        )


def make_token(
    symbol,
    address,
):

    return TokenMarketData(
        symbol=symbol,
        address=address,
        source="test",
    )


@pytest.mark.asyncio
async def test_orchestrator_runs_complete_pipeline():

    market = [
        make_token(
            "SOL",
            "SOL123",
        ),
    ]

    launch = [
        make_token(
            "NEW",
            "NEW123",
        ),
    ]

    scanner = FakeScanner(
        market=market,
        launch=launch,
    )

    intelligence = FakeIntelligence()

    orchestrator = ScanOrchestrator(
        scanner_manager=scanner,
        intelligence_service=intelligence,
    )

    result = await orchestrator.run(
        "SOL"
    )

    assert len(result.market) == 1

    assert len(result.launch) == 1

    assert len(result.combined) == 2


@pytest.mark.asyncio
async def test_orchestrator_deduplicates():

    token = make_token(
        "TEST",
        "SAME123",
    )

    scanner = FakeScanner(
        market=[token],
        launch=[token],
    )

    intelligence = FakeIntelligence()

    orchestrator = ScanOrchestrator(
        scanner_manager=scanner,
        intelligence_service=intelligence,
    )

    result = await orchestrator.run(
        "TEST"
    )

    assert len(result.market) == 1

    assert len(result.launch) == 1

    assert len(result.combined) == 1


@pytest.mark.asyncio
async def test_orchestrator_serialization():

    token = make_token(
        "TEST",
        "TEST123",
    )

    scanner = FakeScanner(
        market=[token],
    )

    intelligence = FakeIntelligence()

    orchestrator = ScanOrchestrator(
        scanner_manager=scanner,
        intelligence_service=intelligence,
    )

    result = await orchestrator.run()

    data = result.to_dict()

    assert "market" in data

    assert "launch" in data

    assert "combined" in data

    assert len(
        data["combined"]
    ) == 1


@pytest.mark.asyncio
async def test_empty_scan():

    scanner = FakeScanner()

    intelligence = FakeIntelligence()

    orchestrator = ScanOrchestrator(
        scanner_manager=scanner,
        intelligence_service=intelligence,
    )

    result = await orchestrator.run()

    assert result.market == []

    assert result.launch == []

    assert result.combined == []