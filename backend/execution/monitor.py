from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.execution_audit import ExecutionAudit
from backend.storage.execution_audit_queries import (
    count_audits,
    list_by_decision,
    list_by_execution_state,
    list_by_gate_status,
)


@dataclass(frozen=True)
class ExecutionMonitoringSummary:
    total: int
    accepted: int
    rejected: int
    watched: int
    strong: int
    gate_approved: int
    gate_blocked: int
    executed: int
    dry_run: int

    @property
    def acceptance_rate(self) -> float:
        if self.total == 0:
            return 0.0

        return (
            self.accepted
            + self.strong
        ) / self.total

    @property
    def execution_rate(self) -> float:
        if self.total == 0:
            return 0.0

        return self.executed / self.total

    @property
    def dry_run_rate(self) -> float:
        if self.total == 0:
            return 0.0

        return self.dry_run / self.total

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "watched": self.watched,
            "strong": self.strong,
            "gate_approved": self.gate_approved,
            "gate_blocked": self.gate_blocked,
            "executed": self.executed,
            "dry_run": self.dry_run,
            "acceptance_rate": self.acceptance_rate,
            "execution_rate": self.execution_rate,
            "dry_run_rate": self.dry_run_rate,
        }


async def build_execution_summary(
    db: AsyncSession,
) -> ExecutionMonitoringSummary:

    total = await count_audits(db)

    accepted = len(
        await list_by_decision(
            db,
            "ACCEPT",
            limit=total or 1,
        )
    )

    rejected = len(
        await list_by_decision(
            db,
            "REJECT",
            limit=total or 1,
        )
    )

    watched = len(
        await list_by_decision(
            db,
            "WATCH",
            limit=total or 1,
        )
    )

    strong = len(
        await list_by_decision(
            db,
            "STRONG",
            limit=total or 1,
        )
    )

    gate_approved = len(
        await list_by_gate_status(
            db,
            approved=True,
            limit=total or 1,
        )
    )

    gate_blocked = len(
        await list_by_gate_status(
            db,
            approved=False,
            limit=total or 1,
        )
    )

    executed = len(
        await list_by_execution_state(
            db,
            executed=True,
            limit=total or 1,
        )
    )

    dry_run = len(
        await list_by_execution_state(
            db,
            dry_run=True,
            limit=total or 1,
        )
    )

    return ExecutionMonitoringSummary(
        total=total,
        accepted=accepted,
        rejected=rejected,
        watched=watched,
        strong=strong,
        gate_approved=gate_approved,
        gate_blocked=gate_blocked,
        executed=executed,
        dry_run=dry_run,
    )