from dataclasses import dataclass

from backend.intelligence.risk_gate import (
    RiskGateResult,
)


@dataclass(frozen=True)
class ExecutionResult:
    """
    Result returned by an execution adapter.

    Package 19 only provides a dry-run implementation.
    No blockchain transaction is created or submitted.
    """

    executed: bool

    dry_run: bool

    decision: str

    score: float

    confidence: float

    risk: float

    message: str

    def to_dict(self) -> dict:
        return {
            "executed": self.executed,
            "dry_run": self.dry_run,
            "decision": self.decision,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "message": self.message,
        }


class DryRunExecutor:
    """
    Safe execution adapter used during development,
    testing, simulation, and paper-trading stages.

    It never submits a blockchain transaction.
    """

    @staticmethod
    def execute(
        gate_result: RiskGateResult,
    ) -> ExecutionResult:

        if not gate_result.approved:

            return ExecutionResult(
                executed=False,
                dry_run=True,
                decision=gate_result.decision,
                score=gate_result.score,
                confidence=gate_result.confidence,
                risk=gate_result.risk,
                message=(
                    "Execution blocked by the risk gate."
                ),
            )

        return ExecutionResult(
            executed=False,
            dry_run=True,
            decision=gate_result.decision,
            score=gate_result.score,
            confidence=gate_result.confidence,
            risk=gate_result.risk,
            message=(
                "Dry-run execution approved. "
                "No transaction was submitted."
            ),
        )