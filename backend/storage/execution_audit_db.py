from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.execution_audit import (
    ExecutionAudit,
)


async def save_execution_audit(
    db: AsyncSession,
    *,
    decision: str,
    score: float,
    confidence: float,
    risk: float,
    gate_approved: bool,
    execution_enabled: bool,
    executed: bool,
    dry_run: bool,
    message: str,
) -> ExecutionAudit:

    record = ExecutionAudit(
        decision=decision,
        score=float(score),
        confidence=float(confidence),
        risk=float(risk),
        gate_approved=bool(
            gate_approved
        ),
        execution_enabled=bool(
            execution_enabled
        ),
        executed=bool(executed),
        dry_run=bool(dry_run),
        message=message,
    )

    db.add(record)

    await db.commit()

    await db.refresh(record)

    return record


async def list_recent_execution_audits(
    db: AsyncSession,
    limit: int = 50,
) -> Sequence[ExecutionAudit]:

    if limit <= 0:
        return []

    result = await db.execute(
        select(ExecutionAudit)
        .order_by(
            ExecutionAudit.created_at.desc(),
            ExecutionAudit.id.desc(),
        )
        .limit(limit)
    )

    return result.scalars().all()