from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = []
last_update = 0


@app.get("/")
def home():
    return {
        "message": "Solana sniper scanner running"
    }


@app.get("/scan")
def scan():

    global cache, last_update

    # ⏱️ cache
    if cache and (time.time() - last_update < 15):
        return JSONResponse(content=cache)

    try:

        # 🔥 Trending searches
        searches = [
            "BONK",
            "WIF",
            "JUP",
            "PYTH",
            "RAY",
            "ORCA",
            "BOME",
            "POPCAT",
            "SAMO",
            "JTO"
        ]

        result = []
        added = set()

        # ==================================
        # 🔥 TRENDING TOKENS
        # ==================================

        for token in searches:

            url = f"https://api.dexscreener.com/latest/dex/search/?q={token}"

            response = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                continue

            data = response.json()

            pairs = data.get("pairs", [])

            for pair in pairs:

                try:

                    chain = pair.get("chainId", "")

                    if chain.lower() != "solana":
                        continue

                    symbol = pair["baseToken"]["symbol"]

                    if symbol in added:
                        continue

                    liquidity = float(
                        pair.get("liquidity", {}).get("usd", 0)
                    )

                    if liquidity < 10000:
                        continue

                    added.add(symbol)

                    result.append({
                        "name": symbol,
                        "price": round(
                            float(pair.get("priceUsd", 0)),
                            6
                        ),
                        "change": round(
                            float(
                                pair.get(
                                    "priceChange",
                                    {}
                                ).get("h24", 0)
                            ),
                            2
                        ),
                        "type": "TRENDING"
                    })

                    break

                except:
                    continue

        # ==================================
        # 🚀 NEW PAIR DETECTOR
        # ==================================

        new_pair_url = (
            "https://api.dexscreener.com/token-profiles/latest/v1"
        )

        response = requests.get(
            new_pair_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:

            data = response.json()

            for token in data[:25]:

                try:

                    chain = token.get("chainId", "")

                    if chain.lower() != "solana":
                        continue

                    symbol = token.get("tokenSymbol", "")

                    if not symbol:
                        continue

                    if symbol in added:
                        continue

                    added.add(symbol)

                    result.append({
                        "name": symbol,
                        "price": 0,
                        "change": 0,
                        "type": "NEW"
                    })

                except:
                    continue

        # 🔥 Sort:
        # NEW pairs first
        # then biggest movers

        result = sorted(
            result,
            key=lambda x: (
                x["type"] != "NEW",
                -abs(x["change"])
            )
        )

        # 💾 cache
        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:

        print("SCAN ERROR:", str(e))

        return JSONResponse(
            content=cache if cache else []
        )