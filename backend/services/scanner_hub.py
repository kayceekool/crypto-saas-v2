from scanners.dex_scanner import DexScanner
from scanners.launch_scanner import LaunchScanner
from scanners.migration_scanner import MigrationScanner


class ScannerHub:

    dex = DexScanner()

    launch = LaunchScanner()

    migration = MigrationScanner()

    @classmethod
    async def scan(cls):

        dex_tokens = await cls.dex.search("sol")

        launches = await cls.launch.scan()

        migrations = await cls.migration.scan()

        return {

            "tokens": dex_tokens,

            "launches": launches,

            "migrations": migrations

        }