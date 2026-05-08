from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import requests
import time

app = FastAPI()

# =========================================
# ✅ CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# CACHE
# =========================================

cache = []
last_update = 0

# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "🚀 Solana sniper engine running"
    }

# =========================================
# SCANNER
# =========================================

@app.get("/scan")
def scan():

    global cache, last_update

    # =====================================
    # CACHE RESPONSE
    # =====================================

    if cache and (time.time() - last_update < 15):

        return JSONResponse(content=cache)

    try:

        # =================================
        # 🔥 TREND SEARCHES
        # =================================

        searches = [

            "solana",
            "ai",
            "meme",
            "dog",
            "cat",
            "pepe",
            "swap",
            "finance",
            "pump",
            "moon",
            "inu",
            "token",
            "dex",
            "launch",
            "new",
            "coin"
        ]

        result = []
        added = set()

        # =================================
        # SEARCH LOOP
        # =================================

        for token in searches:

            try:

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

                # =========================
                # PAIRS LOOP
                # =========================

                for pair in pairs:

                    try:

                        chain = pair.get(
                            "chainId",
                            ""
                        ).lower()

                        # ONLY SOLANA
                        if chain != "solana":
                            continue

                        symbol = pair["baseToken"]["symbol"]

                        # AVOID DUPLICATES
                        if symbol in added:
                            continue

                        price = float(
                            pair.get("priceUsd", 0)
                        )

                        change = float(
                            pair.get(
                                "priceChange",
                                {}
                            ).get(
                                "h24",
                                0
                            )
                        )

                        liquidity = float(
                            pair.get(
                                "liquidity",
                                {}
                            ).get(
                                "usd",
                                0
                            )
                        )

                        volume = float(
                            pair.get(
                                "volume",
                                {}
                            ).get(
                                "h24",
                                0
                            )
                        )

                        fdv = float(
                            pair.get(
                                "fdv",
                                0
                            )
                        )

                        # =====================
                        # MINIMUM FILTERS
                        # =====================

                        if liquidity < 10000:
                            continue

                        if volume < 1000:
                            continue

                        # =====================
                        # 🔥 SNIPER SCORE
                        # =====================

                        score = 0

                        # LIQUIDITY

                        if liquidity > 25000:
                            score += 10

                        if liquidity > 50000:
                            score += 20

                        if liquidity > 100000:
                            score += 20

                        # VOLUME

                        if volume > 10000:
                            score += 10

                        if volume > 50000:
                            score += 20

                        if volume > 100000:
                            score += 20

                        # MOMENTUM

                        if change > 5:
                            score += 10

                        if change > 15:
                            score += 10

                        # FDV

                        if fdv > 500000:
                            score += 10

                        if fdv > 1000000:
                            score += 10

                        # =====================
                        # RATING ENGINE
                        # =====================

                        if score >= 90:
                            rating = "🔥 HOT"

                        elif score >= 70:
                            rating = "🚀 GOOD"

                        elif score >= 40:
                            rating = "👀 WATCH"

                        else:
                            rating = "⚠️ RISKY"

                        # =====================
                        # NEW TOKEN DETECTION
                        # =====================

                        token_type = (
                            "NEW"
                            if liquidity < 50000
                            and volume > 25000
                            else "TRENDING"
                        )

                        added.add(symbol)

                        # =====================
                        # SAVE TOKEN
                        # =====================

                        result.append({

                            "name": symbol,

                            "price": round(
                                price,
                                6
                            ),

                            "change": round(
                                change,
                                2
                            ),

                            "liquidity": round(
                                liquidity,
                                2
                            ),

                            "volume": round(
                                volume,
                                2
                            ),

                            "score": score,

                            "rating": rating,

                            "type": token_type
                        })

                    except:
                        continue

            except:
                continue

        # =================================
        # SORT BY SCORE
        # =================================

        result = sorted(
            result,
            key=lambda x: x["score"],
            reverse=True
        )

        # =================================
        # LIMIT TOKENS
        # =================================

        result = result[:40]

        # =================================
        # UPDATE CACHE
        # =================================

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:

        print(
            "SCAN ERROR:",
            str(e)
        )

        return JSONResponse(
            content=cache if cache else []
        )