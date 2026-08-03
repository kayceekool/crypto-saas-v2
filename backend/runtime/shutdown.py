from backend.core.database import (
    close_db,
)

from backend.core.health import (
    health_manager,
)

from backend.core.logging import (
    get_logger,
)

from backend.core.scheduler import (
    scheduler,
)


logger = get_logger(
    "shutdown"
)


async def shutdown():

    await scheduler.stop()

    health_manager.set_status(
        "scheduler",
        "down",
        "Stopped",
    )


    await close_db()

    health_manager.set_status(
        "database",
        "down",
        "Closed",
    )


    logger.info(
        "Shutdown complete."
    )