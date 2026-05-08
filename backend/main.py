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
    return {"message": "Top Solana scanner running"}


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ cache
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:

        # 🔥 Popular Solana ecosystem tokens
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
            "JTO",
            "NOS",
            "MEW",
            "SLERF",
            "PONKE",
            "MOTHER",
            "GOAT",
            "FWOG",
            "TRUMP",
            "MELANIA"
        ]

        result = []
        added = set()

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

                    # ✅ ONLY SOLANA
                    if chain.lower() != "solana":
                        continue

                    symbol = pair["baseToken"]["symbol"]

                    if symbol in added:
                        continue

                    price = float(pair.get("priceUsd", 0))

                    change = float(
                        pair.get("priceChange", {}).get("h24", 0)
                    )

                    liquidity = float(
                        pair.get("liquidity", {}).get("usd", 0)
                    )

                    # 🚨 skip dead pools
                    if liquidity < 10000:
                        continue

                    added.add(symbol)

                    result.append({
                        "name": symbol,
                        "price": round(price, 6),
                        "change": round(change, 2)
                    })

                    # ✅ take best pair only
                    break

                except:
                    continue

        # 🔥 sort biggest movers
        result = sorted(
            result,
            key=lambda x: abs(x["change"]),
            reverse=True
        )

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=cache if cache else [])