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
    return {"message": "Crypto scanner backend running"}


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ Cache for 20 seconds
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:
        # 🔥 Search top chains/tokens
        searches = [
            "SOL/USDC",
            "BTC/USDT",
            "ETH/USDT",
            "BNB/USDT",
            "XRP/USDT"
        ]

        result = []
        added = set()

        for search in searches:

            url = f"https://api.dexscreener.com/latest/dex/search/?q={search}"

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
                    symbol = pair["baseToken"]["symbol"]

                    price = float(pair.get("priceUsd", 0))

                    change = float(
                        pair.get("priceChange", {}).get("h24", 0)
                    )

                    liquidity = float(
                        pair.get("liquidity", {}).get("usd", 0)
                    )

                    # 🚨 Skip junk/scam pairs
                    if liquidity < 10000:
                        continue

                    # 🚨 Skip duplicate symbols
                    if symbol in added:
                        continue

                    added.add(symbol)

                    result.append({
                        "name": symbol,
                        "price": round(price, 4),
                        "change": round(change, 2)
                    })

                except:
                    continue

        # 🔥 Sort biggest movers first
        result = sorted(
            result,
            key=lambda x: abs(x["change"]),
            reverse=True
        )

        # 💾 Save cache
        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=cache if cache else [])