from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# ✅ CORS
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
        "message": "Solana sniper engine running"
    }


@app.get("/scan")
def scan():

    global cache, last_update

    # ⏱️ cache
    if cache and (time.time() - last_update < 15):
        return JSONResponse(content=cache)

    try:

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
            "KMNO"
        ]

        result = []
        added = set()

        for token in searches:

            url = (
                f"https://api.dexscreener.com/latest/dex/search/?q={token}"
            )

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

                    fdv = float(
                        pair.get("fdv", 0)
                    )

                    # 🚨 minimum filters
                    if liquidity < 10000:
                        continue

                    # =========================
                    # 🔥 SNIPER SCORE ENGINE
                    # =========================

                    score = 0

                    # liquidity
                    if liquidity > 50000:
                        score += 20

                    if liquidity > 100000:
                        score += 20

                    # volume
                    if volume > 25000:
                        score += 20

                    if volume > 100000:
                        score += 20

                    # momentum
                    if change > 5:
                        score += 10

                    if change > 15:
                        score += 10

                    # fdv
                    if fdv > 1000000:
                        score += 10

                    # 🚨 sniper rating
                    if score >= 80:
                        rating = "🔥 HOT"

                    elif score >= 60:
                        rating = "🚀 GOOD"

                    elif score >= 40:
                        rating = "👀 WATCH"

                    else:
                        rating = "⚠️ RISKY"

                    added.add(symbol)

                    result.append({
                        "name": symbol,
                        "price": round(price, 6),
                        "change": round(change, 2),
                        "liquidity": round(liquidity, 2),
                        "volume": round(volume, 2),
                        "score": score,
                        "rating": rating
                    })

                    break

                except:
                    continue

        # 🔥 sort by highest score
        result = sorted(
            result,
            key=lambda x: x["score"],
            reverse=True
        )

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:

        print("SCAN ERROR:", str(e))

        return JSONResponse(
            content=cache if cache else []
        )