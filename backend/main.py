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

    if cache and (time.time() - last_update < 15):

        return JSONResponse(content=cache)

    try:

        searches = [

            "solana",
            "ai",
            "meme",
            "pepe",
            "swap",
            "pump",
            "moon",
            "inu",
            "launch",
            "new",
            "gem",
            "sniper",
            "alpha",
            "100x",
            "microcap"

        ]

        result = []
        added = set()

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

                for pair in pairs:

                    try:

                        chain = (
                            pair.get(
                                "chainId",
                                ""
                            )
                            .lower()
                        )

                        if chain != "solana":
                            continue

                        symbol = (
                            pair["baseToken"]["symbol"]
                            .strip()
                            .upper()
                        )

                        if symbol in added:
                            continue

                        if (
                            len(symbol) > 15
                            or len(symbol) < 2
                        ):
                            continue

                        bad_words = [

                            "HTTP",
                            "WWW",
                            "COM",
                            "ORG",
                            "NET",
                            "TEST",
                            "SCAM",
                            "INUINU",
                            "TOKEN",
                            "COIN",
                            "FINANCE",
                            "DOG",
                            "CAT",
                            "SOL",
                            "ETH"

                        ]

                        if any(
                            bad in symbol
                            for bad in bad_words
                        ):
                            continue

                        price = float(
                            pair.get(
                                "priceUsd",
                                0
                            )
                        )

                        pair_url = pair.get(
                            "url",
                            ""
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

                        if liquidity < 10000:
                            continue

                        if volume < 1000:
                            continue

                        # =================================
                        # SCORE ENGINE
                        # =================================

                        score = 0

                        if liquidity > 25000:
                            score += 10

                        if liquidity > 50000:
                            score += 20

                        if liquidity > 100000:
                            score += 20

                        if liquidity > 500000:
                            score += 20

                        if volume > 10000:
                            score += 10

                        if volume > 50000:
                            score += 20

                        if volume > 100000:
                            score += 20

                        if volume > liquidity * 2:
                            score += 30

                        if change > 3:
                            score += 10

                        if change > 10:
                            score += 20

                        if change > 25:
                            score += 30

                        if change > 50:
                            score += 50

                        if fdv > 500000:
                            score += 10

                        if fdv > 1000000:
                            score += 10

                        # =================================
                        # RATING
                        # =================================

                        if score >= 140:
                            rating = "🚨 EXTREME"

                        elif score >= 110:
                            rating = "🔥 HOT"

                        elif score >= 80:
                            rating = "🚀 GOOD"

                        elif score >= 50:
                            rating = "👀 WATCH"

                        else:
                            rating = "⚠️ RISKY"

                        # =================================
                        # TOKEN TYPE
                        # =================================

                        token_type = (

                            "NEW"

                            if liquidity < 50000
                            and volume > 25000

                            else "TRENDING"
                        )

                        # =================================
                        # RISK ENGINE
                        # =================================

                        risk = "LOW"

                        if liquidity < 30000:
                            risk = "HIGH"

                        elif liquidity < 75000:
                            risk = "MEDIUM"

                        # =================================
                        # BUY SIGNAL ENGINE
                        # =================================

                        buy_signal = "NO"

                        if (
                            score >= 140
                            and change > 15
                            and volume > liquidity
                        ):
                            buy_signal = "STRONG BUY"

                        elif (
                            score >= 100
                            and change > 5
                        ):
                            buy_signal = "BUY"

                        # =================================
                        # SAVE TOKEN
                        # =================================

                        added.add(symbol)

                        result.append({

                            "name": symbol,

                            "price": round(
                                price,
                                8
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

                            "type": token_type,

                            "risk": risk,

                            "signal": buy_signal,

                            "url": pair_url
                        })

                    except:
                        continue

            except:
                continue

        result = sorted(
            result,
            key=lambda x: (
                x["score"],
                x["volume"]
            ),
            reverse=True
        )

        result = result[:40]

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