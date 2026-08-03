from enum import Enum

from backend.core.health import (
    health_manager,
)

from backend.core.logging import (
    get_logger,
)

from backend.core.metrics import (
    metrics,
)


logger = get_logger(
    "lifecycle"
)


class RuntimeState(str, Enum):

    INITIALIZING = (
        "initializing"
    )

    STARTING = "starting"

    RUNNING = "running"

    DEGRADED = "degraded"

    STOPPING = "stopping"

    STOPPED = "stopped"


class Lifecycle:

    def __init__(self):

        self.state = (
            RuntimeState.INITIALIZING
        )


    async def start(self):

        from backend.runtime.startup import (
            startup,
        )

        self.state = (
            RuntimeState.STARTING
        )

        try:

            await startup()

            self.state = (
                RuntimeState.RUNNING
            )

            health_manager.set_status(
                "runtime",
                "up",
                self.state.value,
            )

            logger.info(
                "Runtime is RUNNING. "
                "Uptime baseline: %.3fs",
                metrics.uptime_seconds(),
            )

        except Exception:

            self.state = (
                RuntimeState.DEGRADED
            )

            health_manager.set_status(
                "runtime",
                "down",
                "Startup failed",
            )

            logger.exception(
                "Runtime startup failed."
            )

            raise


    async def stop(self):

        from backend.runtime.shutdown import (
            shutdown,
        )

        self.state = (
            RuntimeState.STOPPING
        )

        await shutdown()

        self.state = (
            RuntimeState.STOPPED
        )

        health_manager.set_status(
            "runtime",
            "down",
            self.state.value,
        )

        logger.info(
            "Runtime is STOPPED."
        )


lifecycle = Lifecycle()