from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db

from backend.execution.monitor import (
    build_execution_summary,
)


router = APIRouter(
    prefix="/execution",
    tags=["execution-monitoring"],
)


@router.get("/summary")
async def execution_summary(
    db: AsyncSession = Depends(get_db),
):
    summary = await build_execution_summary(
        db
    )

    return summary.to_dict()