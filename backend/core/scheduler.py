import asyncio

from collections.abc import (
    Awaitable,
    Callable,
)

from backend.core.logging import (
    get_logger,
)

from backend.core.metrics import (
    metrics,
)

from backend.core.settings import (
    settings,
)


logger = get_logger(
    "scheduler"
)


TaskCallable = Callable[
    [],
    Awaitable[None],
]


class Scheduler:

    def __init__(self):

        self._tasks = {}

        self._jobs = {}

        self._running = False


    def register(
        self,
        name: str,
        callback: TaskCallable,
        interval_seconds: float | None = None,
    ) -> None:

        interval = (
            interval_seconds
            or
            settings.scheduler_interval_seconds
        )

        self._jobs[name] = (
            callback,
            interval,
        )


    async def _runner(
        self,
        name,
        callback,
        interval,
    ):

        while self._running:

            try:

                metrics.tasks_started += 1

                await callback()

            except asyncio.CancelledError:

                raise

            except Exception:

                metrics.task_failures += 1

                logger.exception(
                    "Scheduled task failed: %s",
                    name,
                )

            try:

                await asyncio.sleep(
                    interval
                )

            except asyncio.CancelledError:

                raise


    async def start(self):

        if self._running:

            return

        self._running = True

        for (
            name,
            (
                callback,
                interval,
            ),
        ) in self._jobs.items():

            self._tasks[name] = (
                asyncio.create_task(
                    self._runner(
                        name,
                        callback,
                        interval,
                    ),
                    name=(
                        f"v3-scheduler:"
                        f"{name}"
                    ),
                )
            )

        logger.info(
            "Scheduler started with %d task(s).",
            len(self._tasks),
        )


    async def stop(self):

        if not self._running:

            return

        self._running = False

        tasks = list(
            self._tasks.values()
        )

        self._tasks.clear()

        for task in tasks:

            task.cancel()

        if tasks:

            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        logger.info(
            "Scheduler stopped."
        )


    def snapshot(self):

        return {

            "running":
                self._running,

            "tasks": [

                {
                    "name": name,

                    "done":
                        task.done(),

                    "cancelled":
                        task.cancelled(),
                }

                for (
                    name,
                    task,
                )
                in self._tasks.items()
            ],
        }


scheduler = Scheduler()