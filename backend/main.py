from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import requests
import time

# =========================
# 🚀 IMPORTS
# =========================

try:
    from sniper_engine import discover_new_pairs
except:
    def discover_new_pairs():
        return []

try:
    from exchanges.jupiter import get_jupiter_quote
except:
    def get_jupiter_quote():
        return {"error": "offline"}

app = FastAPI()

# =========================
# 🌐 CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🧠 CACHE
# =========================

scanner_cache = []
sniper_cache = []

last_update = 0

# =========================
# 🏦 ROOT
# =========================

@app.get("/")
def home():

    return {
        "status": "HEDGE_FUND_SAAS_RUNNING",
        "scanner": "ACTIVE",
        "sniper_engine": "ACTIVE",
        "dex": "JUPITER_ENABLED"
    }

# =========================
# ⚡ MAIN SCANNER
# =========================

@app.get("/scan")
def scan():

    global scanner_cache
    global sniper_cache
    global last_update

    # =========================
    # ⚡ RETURN CACHE FAST
    # =========================

    if (
        scanner_cache
        and time.time() - last_update < 15
    ):

        return JSONResponse(content={
            "scanner": scanner_cache,
            "new_pairs": sniper_cache
        })

    try:

        keywords = [
            "pump",
            "ai",
            "sol",
            "meme",
            "cat",
            "dog",
            "pepe",
            "bonk",
            "wojak",
            "launch",
            "moon",
            "gem",
            "100x",
            "alpha",
            "degen",
            "fart"
        ]

        results = []

        added_addresses = set()

        # =========================
        # 🔍 MAIN SCANNER LOOP
        # =========================

        for keyword in keywords:

            try:

                response = requests.get(
                    f"https://api.dexscreener.com/latest/dex/search/?q={keyword}",
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

                        chain = pair.get(
                            "chainId",
                            ""
                        ).lower()

                        if chain != "solana":
                            continue

                        pair_address = pair.get(
                            "pairAddress",
                            ""
                        )

                        if pair_address in added_addresses:
                            continue

                        added_addresses.add(pair_address)

                        symbol = pair["baseToken"]["symbol"]

                        price = float(
                            pair.get("priceUsd", 0)
                        )

                        change = float(
                            pair.get(
                                "priceChange",
                                {}
                            ).get("h24", 0)
                        )

                        liquidity = float(
                            pair.get(
                                "liquidity",
                                {}
                            ).get("usd", 0)
                        )

                        volume = float(
                            pair.get(
                                "volume",
                                {}
                            ).get("h24", 0)
                        )

                        fdv = float(
                            pair.get("fdv", 0)
                        )

                        dex_url = (
                            f"https://dexscreener.com/solana/{pair_address}"
                        )

                        # =========================
                        # 🚨 BASIC FILTERS
                        # =========================

                        if liquidity < 10000:
                            continue

                        # =========================
                        # 🚀 REAL NEW TOKEN DETECTION
                        # =========================

                        pair_created = pair.get(
                            "pairCreatedAt",
                            0
                        )

                        age_minutes = 999999

                        if pair_created:

                            age_minutes = (
                                time.time() -
                                (pair_created / 1000)
                            ) / 60

                        if age_minutes <= 360:

                            token_type = "NEW"

                        else:

                            token_type = "TRENDING"

                        # =========================
                        # 🧠 INSTITUTIONAL AI ENGINE
                        # =========================

                        score = 0

                        # liquidity quality

                        if liquidity > 20000:
                            score += 20

                        if liquidity > 50000:
                            score += 30

                        if liquidity > 100000:
                            score += 40

                        if liquidity > 500000:
                            score += 50

                        # volume strength

                        if volume > 10000:
                            score += 20

                        if volume > 50000:
                            score += 30

                        if volume > 100000:
                            score += 40

                        if volume > 500000:
                            score += 50

                        # momentum

                        if change > 3:
                            score += 20

                        if change > 8:
                            score += 30

                        if change > 15:
                            score += 40

                        if change > 30:
                            score += 60

                        if change > 100:
                            score += 120

                        if change > 500:
                            score += 200

                        if change > 1000:
                            score += 300

                        # volume/liquidity ratio

                        if liquidity > 0:

                            ratio = volume / liquidity

                            if ratio > 0.5:
                                score += 20

                            if ratio > 1:
                                score += 40

                            if ratio > 2:
                                score += 60

                            if ratio > 5:
                                score += 120

                        # low cap detection

                        if fdv > 0 and fdv < 500000:
                            score += 40

                        if fdv > 0 and fdv < 200000:
                            score += 80

                        # early trend engine

                        if (
                            liquidity > 30000
                            and volume > liquidity
                            and change > 10
                        ):
                            score += 80

                        # viral breakout engine

                        if (
                            volume > liquidity * 3
                            and change > 25
                        ):
                            score += 150

                        # smart money

                        if (
                            liquidity > 100000
                            and volume > 200000
                            and change > 15
                        ):
                            score += 100

                        # microcap sniper

                        if (
                            liquidity < 100000
                            and volume > 500000
                            and change > 20
                        ):
                            score += 150

                        # =========================
                        # 🚨 AI RATING ENGINE
                        # =========================

                        if score >= 700:

                            rating = "👑 GOD CANDLE"

                        elif score >= 500:

                            rating = "🚀 PARABOLIC"

                        elif score >= 300:

                            rating = "💎 GEM"

                        elif score >= 180:

                            rating = "🚨 EXTREME"

                        elif score >= 120:

                            rating = "🔥 HOT"

                        elif score >= 80:

                            rating = "🚀 GOOD"

                        elif score >= 50:

                            rating = "👀 WATCH"

                        else:

                            rating = "⚠️ RISKY"

                        # =========================
                        # 🛡️ RISK ENGINE
                        # =========================

                        if liquidity > 100000:

                            risk = "LOW"

                        elif liquidity > 40000:

                            risk = "MEDIUM"

                        else:

                            risk = "HIGH"

                        # =========================
                        # 📡 AI SIGNAL ENGINE
                        # =========================

                        if score >= 700:

                            signal = "ULTRA SEND"

                        elif score >= 500:

                            signal = "PARABOLIC"

                        elif score >= 300:

                            signal = "SNIPER ENTRY"

                        elif score >= 180:

                            signal = "STRONG BUY"

                        elif score >= 120:

                            signal = "BUY"

                        else:

                            signal = "NO"

                        # =========================
                        # ⚡ JUPITER CHECK
                        # =========================

                        jupiter = get_jupiter_quote()

                        results.append({

                            "type": token_type,

                            "name": symbol.upper(),

                            "price": round(price, 8),

                            "change": round(change, 2),

                            "liquidity": round(liquidity, 2),

                            "volume": round(volume, 2),

                            "score": score,

                            "rating": rating,

                            "risk": risk,

                            "signal": signal,

                            "url": dex_url,

                            "jupiter": (
                                "ONLINE"
                                if "error" not in jupiter
                                else "OFFLINE"
                            )
                        })

                    except:
                        continue

            except:
                continue

        # =========================
        # 🚀 SOL SNIPER ENGINE
        # =========================

        sniper_pairs = discover_new_pairs()

        # =========================
        # 📊 SORT
        # =========================

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # limit dashboard size

        results = results[:15]

        scanner_cache = results
        sniper_cache = sniper_pairs

        last_update = time.time()

        return JSONResponse(content={

            "scanner": results,

            "new_pairs": sniper_pairs

        })

    except Exception as e:

        print("SCAN ERROR:", str(e))

        return JSONResponse(content={

            "scanner": scanner_cache,

            "new_pairs": sniper_cache,

            "error": str(e)

        })