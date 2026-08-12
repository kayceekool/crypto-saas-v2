from backend.intelligence.confidence import (
    ConfidenceEngine,
)

from backend.intelligence.launch import (
    LaunchAI,
)

from backend.intelligence.migration import (
    MigrationAI,
)

from backend.intelligence.models import (
    IntelligenceResult,
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


class MasterAI:

    def __init__(self):

        self.confidence = (
            ConfidenceEngine()
        )

    @staticmethod
    def classify_risk(
        token: TokenMarketData,
    ) -> str:

        liquidity = token.liquidity_usd

        volume = token.volume_24h_usd

        if liquidity <= 0:

            return "HIGH"

        if liquidity < 5000:

            return "HIGH"

        if liquidity < 25000:

            return "MEDIUM"

        if volume < 1000:

            return "MEDIUM"

        return "LOW"

    @staticmethod
    def classify_signal(
        score: float,
        confidence: float,
        risk: str,
    ) -> str:

        if risk == "HIGH":

            return "AVOID"

        if (
            score >= 1000
            and confidence >= 70
        ):

            return "STRONG"

        if (
            score >= 600
            and confidence >= 55
        ):

            return "WATCH"

        return "NEUTRAL"

    def analyze(
        self,
        token: TokenMarketData,
    ) -> IntelligenceResult:

        base_score = (
            ScoringEngine.calculate(
                token
            )
        )

        pattern, pattern_adjustment = (
            PatternAI.detect(
                token,
                base_score,
            )
        )

        launch_adjustment = (
            LaunchAI.score(
                token
            )
        )

        migration_adjustment = (
            MigrationAI.score(
                token
            )
        )

        final_score = (
            base_score
            + pattern_adjustment
            + launch_adjustment
            + migration_adjustment
        )

        risk = self.classify_risk(
            token
        )

        confidence = (
            self.confidence.calculate(
                score=final_score,
                pattern=pattern,
                risk=risk,
            )
        )

        signal = self.classify_signal(
            final_score,
            confidence,
            risk,
        )

        return IntelligenceResult(
            token=token,
            base_score=base_score,
            pattern_adjustment=(
                pattern_adjustment
            ),
            launch_adjustment=(
                launch_adjustment
            ),
            migration_adjustment=(
                migration_adjustment
            ),
            final_score=round(
                final_score,
                2,
            ),
            confidence=confidence,
            pattern=pattern,
            risk=risk,
            signal=signal,
        )