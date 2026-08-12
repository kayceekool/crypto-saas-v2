from backend.intelligence.confidence import (
    ConfidenceEngine,
)

from backend.intelligence.launch import (
    LaunchAI,
)

from backend.intelligence.master import (
    MasterAI,
)

from backend.intelligence.migration import (
    MigrationAI,
)

from backend.intelligence.pattern import (
    PatternAI,
)

from backend.intelligence.scoring import (
    ScoringEngine,
)

from backend.providers.models import (
    TokenMarketData,
)

from backend.services.intelligence_service import (
    IntelligenceService,
)


def make_token(
    *,
    symbol="TEST",
    liquidity=50000.0,
    volume=100000.0,
    age=2.0,
):

    return TokenMarketData(

        symbol=symbol,

        address=f"{symbol}_ADDRESS",

        liquidity_usd=liquidity,

        volume_24h_usd=volume,

        age_hours=age,

        source="test",
    )


def test_scoring_engine():

    token = make_token(
        liquidity=50000,
        volume=100000,
        age=2,
    )

    score = ScoringEngine.calculate(
        token
    )

    assert score > 0


def test_launch_ai():

    token = make_token(
        age=0.5,
        liquidity=30000,
    )

    adjustment = LaunchAI.score(
        token
    )

    assert adjustment == 200


def test_pattern_breakout():

    token = make_token(
        liquidity=10000,
        volume=50000,
    )

    pattern, adjustment = (
        PatternAI.detect(
            token,
            900,
        )
    )

    assert pattern == "BREAKOUT"

    assert adjustment == 150


def test_pattern_accumulation():

    token = make_token(
        liquidity=10000,
        volume=20000,
    )

    pattern, adjustment = (
        PatternAI.detect(
            token,
            600,
        )
    )

    assert pattern == "ACCUMULATION"

    assert adjustment == 75


def test_migration_ai():

    token = make_token(
        volume=60000,
    )

    token.metadata = {
        "migrated": True,
        "raydium": True,
    }

    adjustment = MigrationAI.score(
        token
    )

    assert adjustment == 200


def test_confidence_bounds():

    engine = ConfidenceEngine()

    confidence = engine.calculate(
        score=2000,
        pattern="BREAKOUT",
        risk="LOW",
    )

    assert confidence <= 99

    assert confidence >= 5


def test_master_ai():

    token = make_token(
        liquidity=50000,
        volume=100000,
        age=0.5,
    )

    engine = MasterAI()

    result = engine.analyze(
        token
    )

    assert result.final_score > 0

    assert result.confidence >= 5

    assert result.confidence <= 99

    assert result.pattern in {
        "BREAKOUT",
        "ACCUMULATION",
        "NORMAL",
    }

    assert result.risk in {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    assert result.signal in {
        "STRONG",
        "WATCH",
        "NEUTRAL",
        "AVOID",
    }


def test_intelligence_service():

    tokens = [

        make_token(
            symbol="AAA",
            liquidity=50000,
            volume=100000,
            age=1,
        ),

        make_token(
            symbol="BBB",
            liquidity=5000,
            volume=1000,
            age=10,
        ),
    ]

    service = IntelligenceService()

    results = service.rank(
        tokens
    )

    assert len(results) == 2

    assert (
        results[0].final_score
        >= results[1].final_score
    )


def test_result_serialization():

    token = make_token()

    result = MasterAI().analyze(
        token
    )

    data = result.to_dict()

    assert "token" in data

    assert "final_score" in data

    assert "confidence" in data

    assert "risk" in data

    assert "signal" in data