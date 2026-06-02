import asyncio

from scanners.launch_scanner import launch_loop
from scanners.dex_loop import dex_loop
from scanners.migration_scanner import migration_loop
from scanners.wallet_scanner import wallet_loop
from services.alert_engine import AlertEngine
from services.ranking_engine import RankingEngine
asyn
c def start_scheduler():

    asyncio.create_task(
        dex_loop()
    )

    asyncio.create_task(
        launch_loop()
    )

    asyncio.create_task(
        migration_loop()
    )

    asyncio.create_task(
        wallet_loop()
    )

    print(
        "All scanner tasks started"
    )