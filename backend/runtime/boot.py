from backend.runtime.lifecycle import (
    lifecycle,
)


async def boot():

    """
    Explicit programmatic boot hook
    for tests and tooling.
    """

    await lifecycle.start()