from sqlalchemy.ext.asyncio import AsyncSession

from backend.execution.audit import (
    ExecutionAuditRecord,
)

from backend.execution.audited_executor import (
    AuditedDryRunExecutor,
)

from backend.execution.audit_store import (
    ExecutionAuditStore,
)

from backend.execution.dry_run import (
    ExecutionResult,
)

from backend.storage.execution_audit_db import (
    save_execution_audit,
)

from backend.intelligence.risk_gate import (
    RiskGateResult,
)


class PersistentAuditedDryRunExecutor:
    """
    Dry-run executor that records every execution
    decision in the persistent database.

    No real blockchain transaction is submitted.
    """

    def __init__(
        self,
        db: AsyncSession,
        audit_store: ExecutionAuditStore | None = None,
    ) -> None:

        self.db = db

        self.audit_store = (
            audit_store
            if audit_store is not None
            else ExecutionAuditStore()
        )

        self.executor = (
            AuditedDryRunExecutor(
                audit_store=self.audit_store
            )
        )

    async def execute(
        self,
        gate_result: RiskGateResult,
    ) -> ExecutionResult:

        result = self.executor.execute(
            gate_result
        )

        audit_record = (
            self.audit_store.recent(1)[0]
        )

        await save_execution_audit(
            self.db,
            decision=audit_record.decision,
            score=audit_record.score,
            confidence=audit_record.confidence,
            risk=audit_record.risk,
            gate_approved=(
                audit_record.gate_approved
            ),
            execution_enabled=(
                audit_record.execution_enabled
            ),
            executed=audit_record.executed,
            dry_run=audit_record.dry_run,
            message=audit_record.message,
        )

        return result