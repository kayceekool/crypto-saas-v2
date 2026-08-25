from dataclasses import dataclass

from backend.intelligence.decision import (
    IntelligenceDecision,
)


@dataclass(frozen=True)
class RiskGateResult:
    """
    Result of the final pre-execution risk gate.

    The gate only approves or blocks a decision.
    It never executes an order or transaction.
    """

    approved: bool

    decision: str

    score: float

    confidence: float

    risk: float

    reason: str

    def to_dict(self) -> dict:
        return {
            "approved": self.approved,
            "decision": self.decision,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "reason": self.reason,
        }


class RiskGate:
    """
    Conservative pre-execution risk gate.

    Approval requires:

    1. Explicit execution eligibility.
    2. STRONG or ACCEPT decision.
    3. Minimum score.
    4. Minimum confidence.
    5. Maximum risk.

    WATCH and REJECT decisions are never approved.

    This class does not execute trades.
    """

    MIN_APPROVED_SCORE = 650.0

    MIN_APPROVED_CONFIDENCE = 60.0

    MAX_APPROVED_RISK = 50.0

    APPROVED_DECISIONS = frozenset(
        {
            "STRONG",
            "ACCEPT",
        }
    )

    @classmethod
    def evaluate(
        cls,
        decision: IntelligenceDecision,
        execution_enabled: bool = False,
    ) -> RiskGateResult:

        score = float(
            decision.score
        )

        confidence = float(
            decision.confidence
        )

        risk = float(
            decision.risk
        )

        if not execution_enabled:
            return RiskGateResult(
                approved=False,
                decision=decision.decision,
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Execution is not explicitly enabled."
                ),
            )

        if (
            decision.decision
            not in cls.APPROVED_DECISIONS
        ):
            return RiskGateResult(
                approved=False,
                decision=decision.decision,
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Decision classification is not "
                    "eligible for approval."
                ),
            )

        if score < cls.MIN_APPROVED_SCORE:
            return RiskGateResult(
                approved=False,
                decision=decision.decision,
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Score is below the minimum "
                    "risk-gate threshold."
                ),
            )

        if (
            confidence
            < cls.MIN_APPROVED_CONFIDENCE
        ):
            return RiskGateResult(
                approved=False,
                decision=decision.decision,
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Confidence is below the minimum "
                    "risk-gate threshold."
                ),
            )

        if risk > cls.MAX_APPROVED_RISK:
            return RiskGateResult(
                approved=False,
                decision=decision.decision,
                score=score,
                confidence=confidence,
                risk=risk,
                reason=(
                    "Risk exceeds the maximum "
                    "risk-gate threshold."
                ),
            )

        return RiskGateResult(
            approved=True,
            decision=decision.decision,
            score=score,
            confidence=confidence,
            risk=risk,
            reason=(
                "Signal passed all risk-gate checks."
            ),
        )