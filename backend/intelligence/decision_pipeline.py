from dataclasses import dataclass

from backend.intelligence.decision import (
    IntelligenceDecision,
    IntelligenceDecisionEngine,
)

from backend.intelligence.pipeline import (
    IntelligencePipeline,
)


@dataclass(frozen=True)
class IntelligenceDecisionResult:
    """
    Complete intelligence evaluation result.

    This object combines historical feedback,
    calibration, adjusted signal values, and the
    final intelligence classification.

    It does not execute trades.
    """

    intelligence: object

    decision: IntelligenceDecision

    def to_dict(self) -> dict:
        return {
            "intelligence": (
                self.intelligence.to_dict()
            ),
            "decision": (
                self.decision.to_dict()
            ),
        }


class IntelligenceDecisionPipeline:
    """
    Final orchestration layer for intelligence evaluation.

    Flow:

        Historical records
              ↓
        IntelligencePipeline
              ↓
        Adjusted signal
              ↓
        Decision Engine
              ↓
        IntelligenceDecisionResult
    """

    @classmethod
    def evaluate(
        cls,
        historical_records,
        score: float,
        confidence: float,
        risk: float,
    ) -> IntelligenceDecisionResult:

        intelligence = (
            IntelligencePipeline.evaluate(
                historical_records=historical_records,
                score=score,
                confidence=confidence,
                risk=risk,
            )
        )

        decision = (
            IntelligenceDecisionEngine.evaluate(
                intelligence.adjusted_signal
            )
        )

        return IntelligenceDecisionResult(
            intelligence=intelligence,
            decision=decision,
        )