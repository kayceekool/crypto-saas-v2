from backend.execution.audit import (
    ExecutionAuditRecord,
)

from backend.execution.audit_store import (
    ExecutionAuditStore,
)

from backend.execution.dry_run import (
    DryRunExecutor,
    ExecutionResult,
)

from backend.intelligence.risk_gate import (
    RiskGateResult,
)


class AuditedDryRunExecutor:
    """
    Dry-run executor with an audit trail.

    Every execution attempt produces an immutable
    audit record.

    No real transaction is submitted.
    """

    def __init__(
        self,
        audit_store: ExecutionAuditStore | None = None,
    ) -> None:

        self.audit_store = (
            audit_store
            if audit_store is not None
            else ExecutionAuditStore()
        )

    def execute(
        self,
        gate_result: RiskGateResult,
    ) -> ExecutionResult:

        result = DryRunExecutor.execute(
            gate_result
        )

        audit_record = (
            ExecutionAuditRecord.from_execution(
                decision=result.decision,
                score=result.score,
                confidence=result.confidence,
                risk=result.risk,
                gate_approved=(
                    gate_result.approved
                ),
                execution_enabled=(
                    gate_result.approved
                ),
                executed=result.executed,
                dry_run=result.dry_run,
                message=result.message,
            )
        )

        self.audit_store.add(
            audit_record
        )

        return result