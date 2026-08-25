from collections.abc import Iterable

from backend.execution.audit import (
    ExecutionAuditRecord,
)


class ExecutionAuditStore:
    """
    In-memory execution audit store.

    Package 22 deliberately keeps persistence out of this
    component. It provides a clean interface that can later
    be backed by the application's database.

    No transaction execution occurs here.
    """

    def __init__(
        self,
        records: Iterable[
            ExecutionAuditRecord
        ] | None = None,
    ) -> None:

        self._records = list(
            records or []
        )

    def add(
        self,
        record: ExecutionAuditRecord,
    ) -> ExecutionAuditRecord:

        self._records.append(record)

        return record

    def count(self) -> int:

        return len(self._records)

    def all(
        self,
    ) -> list[ExecutionAuditRecord]:

        return list(self._records)

    def recent(
        self,
        limit: int = 50,
    ) -> list[ExecutionAuditRecord]:

        if limit <= 0:
            return []

        return list(
            reversed(
                self._records[-limit:]
            )
        )

    def clear(self) -> None:

        self._records.clear()