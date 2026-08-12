from backend.core.database import (
    init_db,
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

from backend.core.provider_registry import (
    provider_registry,
)

from backend.providers.dexscreener.provider import (
    DexScreenerProvider,
)

from backend.providers.pumpfun.provider import (
    PumpFunProvider,
)

from backend.providers.helius.provider import (
    HeliusProvider,
)


logger = get_logger(
    "startup"
)


async def startup():

    # Database

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


    # Providers

    dexscreener = (
        DexScreenerProvider()
    )

    pumpfun = (
        PumpFunProvider()
    )

    helius = (
        HeliusProvider()
    )


    provider_registry.register(
        "dexscreener",
        dexscreener,
        priority=10,
    )

    provider_registry.register(
        "pumpfun",
        pumpfun,
        priority=20,
    )

    provider_registry.register(
        "helius",
        helius,
        priority=30,
    )


    health_manager.set_status(
        "providers",
        "up",
        "Provider registry initialized",
    )


    # Scheduler

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