import requests
import time

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/search"

seen_tokens = set()

def discover_new_pairs():

    keywords = [
        "pump",
        "ai",
        "sol",
        "meme",
        "cat",
        "dog"
    ]

    discovered = []

    for k in keywords:

        try:

            response = requests.get(
                f"{DEXSCREENER_URL}/?q={k}",
                timeout=10
            )

            pairs = response.json().get("pairs", [])

            for pair in pairs:

                try:

                    if pair.get("chainId", "").lower() != "solana":
                        continue

                    symbol = pair["baseToken"]["symbol"]

                    if symbol in seen_tokens:
                        continue

                    liquidity = float(
                        pair.get("liquidity", {}).get("usd", 0)
                    )

                    volume = float(
                        pair.get("volume", {}).get("h24", 0)
                    )

                    if liquidity < 10000:
                        continue

                    seen_tokens.add(symbol)

                    discovered.append({
                        "symbol": symbol,
                        "pairAddress": pair.get("pairAddress"),
                        "liquidity": liquidity,
                        "volume": volume,
                        "price": pair.get("priceUsd", 0)
                    })

                except:
                    continue

        except:
            continue

    return discovered