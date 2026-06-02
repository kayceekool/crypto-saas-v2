import asyncio

from scanners.dex_scanner import DexScanner

scanner = DexScanner()

SEARCH_TERMS = [
    "pump",
    "meme",
    "launch",
    "sol",
    "ai",
    "bonk",
    "pepe",
    "new"
]

async def dex_loop():

    while True:

        try:

            for term in SEARCH_TERMS:

                result = await scanner.search(
                    term
                )

                pair_count = len(
                    result.get(
                        "pairs",
                        []
                    )
                )

                print(
                    f"[DEX] {term} -> {pair_count}"
                )

        except Exception as e:

            print(
                "[DEX ERROR]",
                e
            )

        await asyncio.sleep(15)