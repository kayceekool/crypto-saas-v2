from core.database import (
    AsyncSessionLocal
)


class DatabaseService:

    @staticmethod
    async def session():

        async with (
            AsyncSessionLocal()
        ) as session:

            yield session