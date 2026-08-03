from dataclasses import dataclass, field
from time import monotonic


@dataclass
class Metrics:

    started_at: float = field(
        default_factory=monotonic
    )

    events_processed: int = 0

    tasks_started: int = 0

    task_failures: int = 0

    def uptime_seconds(self) -> float:

        return round(
            monotonic() - self.started_at,
            3,
        )

    def snapshot(self) -> dict:

        return {
            "uptime_seconds":
                self.uptime_seconds(),

            "events_processed":
                self.events_processed,

            "tasks_started":
                self.tasks_started,

            "task_failures":
                self.task_failures,
        }


metrics = Metrics()