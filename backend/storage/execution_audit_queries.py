from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.execution_audit import (
    ExecutionAudit,
)


async def list_by_decision(
    db: AsyncSession,
    decision: str,
    limit: int = 50,
) -> Sequence[ExecutionAudit]:

    if limit <= 0:
        return []

    result = await db.execute(
        select(ExecutionAudit)
        .where(
            ExecutionAudit.decision
            == decision
        )
        .order_by(
            ExecutionAudit.created_at.desc(),
            ExecutionAudit.id.desc(),
        )
        .limit(limit)
    )

    return result.scalars().all()


async def list_by_execution_state(
    db: AsyncSession,
    *,
    executed: bool | None = None,
    dry_run: bool | None = None,
    limit: int = 50,
) -> Sequence[ExecutionAudit]:

    if limit <= 0:
        return []

    statement = select(
        ExecutionAudit
    )

    if executed is not None:
        statement = statement.where(
            ExecutionAudit.executed
            == executed
        )

    if dry_run is not None:
        statement = statement.where(
            ExecutionAudit.dry_run
            == dry_run
        )

    statement = (
        statement
        .order_by(
            ExecutionAudit.created_at.desc(),
            ExecutionAudit.id.desc(),
        )
        .limit(limit)
    )

    result = await db.execute(
        statement
    )

    return result.scalars().all()


async def list_by_gate_status(
    db: AsyncSession,
    *,
    approved: bool,
    limit: int = 50,
) -> Sequence[ExecutionAudit]:

    if limit <= 0:
        return []

    result = await db.execute(
        select(ExecutionAudit)
        .where(
            ExecutionAudit.gate_approved
            == approved
        )
        .order_by(
            ExecutionAudit.created_at.desc(),
            ExecutionAudit.id.desc(),
        )
        .limit(limit)
    )

    return result.scalars().all()


async def count_audits(
    db: AsyncSession,
) -> int:

    result = await db.execute(
        select(
            func.count(
                ExecutionAudit.id
            )
        )
    )

    return int(
        result.scalar_one()
    )