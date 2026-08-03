from backend.core.database import (
    init_db,
)

from backend.core.health import (
    health_manager,
)

from backend.core.logging import (
    get_logger,
)

from backend.core.plugin_loader import (
    plugin_loader,
)

from backend.core.provider_registry import (
    provider_registry,
)

from backend.core.scheduler import (
    scheduler,
)


logger = get_logger(
    "startup"
)


async def startup():

    health_manager.set_status(
        "database",
        "degraded",
        "initializing",
    )

    await init_db()

    health_manager.set_status(
        "database",
        "up",
        "SQLite/SQLAlchemy initialized",
    )


    health_manager.set_status(
        "providers",
        "up",
        "Registry initialized",
    )


    health_manager.set_status(
        "plugins",
        "up",
        "Plugin loader initialized",
    )


    async def runtime_heartbeat():

        health_manager.set_status(
            "scheduler",
            "up",
            "Scheduler heartbeat",
        )


    scheduler.register(
        "runtime-heartbeat",
        runtime_heartbeat,
        interval_seconds=15,
    )


    await scheduler.start()


    health_manager.set_status(
        "scheduler",
        "up",
        "Background scheduler running",
    )


    logger.info(
        "Startup complete."
    )