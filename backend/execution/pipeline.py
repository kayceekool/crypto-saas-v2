from dataclasses import dataclass

from backend.execution.dry_run import (
    DryRunExecutor,
    ExecutionResult,
)

from backend.intelligence.decision_pipeline import (
    IntelligenceDecisionPipeline,
)

from backend.intelligence.risk_gate import (
    RiskGate,
    RiskGateResult,
)


@dataclass(frozen=True)
class ExecutionPipelineResult:
    """
    Complete end-to-end dry-run evaluation.

    Flow:

        signal
          ↓
        intelligence
          ↓
        decision
          ↓
        risk gate
          ↓
        dry-run executor

    No real transaction is submitted.
    """

    intelligence: object

    gate: RiskGateResult

    execution: ExecutionResult

    def to_dict(self) -> dict:
        return {
            "intelligence": (
                self.intelligence.to_dict()
            ),
            "gate": (
                self.gate.to_dict()
            ),
            "execution": (
                self.execution.to_dict()
            ),
        }


class ExecutionPipeline:
    """
    End-to-end safe execution pipeline.

    Package 20 intentionally supports dry-run
    execution only.
    """

    @classmethod
    def evaluate(
        cls,
        historical_records,
        score: float,
        confidence: float,
        risk: float,
        execution_enabled: bool = False,
    ) -> ExecutionPipelineResult:

        intelligence = (
            IntelligenceDecisionPipeline.evaluate(
                historical_records=historical_records,
                score=score,
                confidence=confidence,
                risk=risk,
            )
        )

        gate = RiskGate.evaluate(
            decision=intelligence.decision,
            execution_enabled=execution_enabled,
        )

        execution = DryRunExecutor.execute(
            gate
        )

        return ExecutionPipelineResult(
            intelligence=intelligence,
            gate=gate,
            execution=execution,
        )