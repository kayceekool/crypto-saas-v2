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
    return {"message": "Solana scanner backend running"}


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ Cache for 20 seconds
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:
        # 🔥 DexScreener Solana pairs endpoint
        url = "https://api.dexscreener.com/latest/dex/pairs/solana"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            return JSONResponse(content=[])

        data = response.json()

        pairs = data.get("pairs", [])

        result = []
        added = set()

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

                volume = float(
                    pair.get("volume", {}).get("h24", 0)
                )

                # 🚨 Skip junk
                if liquidity < 50000:
                    continue

                if volume < 10000:
                    continue

                # 🚨 Skip duplicates
                if symbol in added:
                    continue

                added.add(symbol)

                result.append({
                    "name": symbol,
                    "price": round(price, 6),
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

        # 🔥 Limit top 50
        result = result[:50]

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=cache if cache else [])