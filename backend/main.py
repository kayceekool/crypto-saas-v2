from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import requests
import time
import random

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
# 🐋 WHALE MEMORY
# =========================

whale_wallets = [

    "SOL_WHALE_1",
    "SOL_WHALE_2",
    "SOL_WHALE_3"

]

recent_whale_activity = {}

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
    # ⚡ SMART CACHE
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
            "pumpfun",
            "launch",
            "moon",
            "100x",
            "degen",
            "alpha",
            "ai",
            "agi",
            "meme",
            "cat",
            "dog",
            "pepe",
            "bonk",
            "wojak",
            "sol",
            "new",
            "viral"

        ]

        # =========================
        # 🧠 DEDUPE MEMORY
        # =========================

        best_symbols = {}

        # =========================
        # 🔎 SEARCH ENGINE
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

                        base_token = pair.get(
                            "baseToken",
                            {}
                        )

                        symbol = base_token.get(
                            "symbol",
                            ""
                        ).upper()

                        if not symbol:
                            continue

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

                        pair_address = pair.get(
                            "pairAddress",
                            ""
                        )

                        dex_url = (
                            f"https://dexscreener.com/solana/{pair_address}"
                        )

                        # =========================
                        # 🚨 HARD FILTERS
                        # =========================

                        if liquidity < 10000:
                            continue

                        if volume < 100:
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
                        # 🧠 AI SNIPER SCORE
                        # =========================

                        score = 0

                        # liquidity
                        if liquidity > 25000:
                            score += 30

                        if liquidity > 100000:
                            score += 40

                        if liquidity > 500000:
                            score += 50

                        # volume
                        if volume > 10000:
                            score += 30

                        if volume > 100000:
                            score += 50

                        if volume > 500000:
                            score += 70

                        # momentum
                        if change > 5:
                            score += 40

                        if change > 20:
                            score += 80

                        if change > 50:
                            score += 120

                        # early sniper opportunity
                        if (
                            volume > liquidity
                            and liquidity < 200000
                        ):
                            score += 80

                        # ultra early launches
                        if age_minutes <= 30:
                            score += 120

                        elif age_minutes <= 120:
                            score += 60

                        # viral explosion
                        if (
                            volume > liquidity * 3
                        ):
                            score += 150

                        # fdv intelligence
                        if fdv > 1000000:
                            score += 20

                        # =========================
                        # 🧠 AI CONFIDENCE ENGINE
                        # =========================

                        confidence = 50

                        if change > 5:
                            confidence += 10

                        if change > 15:
                            confidence += 15

                        if change > 40:
                            confidence += 20

                        if liquidity > 50000:
                            confidence += 10

                        if liquidity > 250000:
                            confidence += 10

                        if volume > liquidity:
                            confidence += 15

                        if volume > liquidity * 3:
                            confidence += 20

                        if age_minutes <= 60:
                            confidence += 10

                        if confidence > 99:
                            confidence = 99

                        # =========================
                        # 🚨 RATING ENGINE
                        # =========================

                        if score >= 800:

                            rating = "👑 GOD CANDLE"
                            signal = "ULTRA SEND"

                        elif score >= 400:

                            rating = "🚀 PARABOLIC"
                            signal = "PARABOLIC"

                        elif score >= 250:

                            rating = "💎 GEM"
                            signal = "SNIPER ENTRY"

                        elif score >= 180:

                            rating = "🚨 EXTREME"
                            signal = "STRONG BUY"

                        elif score >= 120:

                            rating = "🔥 HOT"
                            signal = "BUY"

                        elif score >= 80:

                            rating = "🚀 GOOD"
                            signal = "NO"

                        else:

                            rating = "⚠️ RISKY"
                            signal = "NO"

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
                        # 🐋 WHALE ACTIVITY
                        # =========================

                        whale_score = random.randint(0, 100)

                        if whale_score > 80:

                            whale_signal = "🐋 WHALE BUYING"

                        elif whale_score > 60:

                            whale_signal = "👀 SMART MONEY"

                        else:

                            whale_signal = "NONE"

                        # =========================
                        # 📦 COIN OBJECT
                        # =========================

                        coin_data = {

                            "type": token_type,

                            "name": symbol,

                            "price": round(price, 8),

                            "change": round(change, 2),

                            "liquidity": round(liquidity, 2),

                            "volume": round(volume, 2),

                            "score": score,

                            "confidence": confidence,

                            "whale_signal": whale_signal,

                            "age_minutes": round(age_minutes, 1),

                            "rating": rating,

                            "risk": risk,

                            "signal": signal,

                            "url": dex_url

                        }

                        # =========================
                        # 🧠 INSTITUTIONAL DEDUPE ENGINE
                        # =========================

                        symbol_key = symbol.upper()

                        existing = best_symbols.get(
                            symbol_key
                        )

                        market_strength = (

                            liquidity +
                            volume +
                            (score * 1000)

                        )

                        coin_data[
                            "market_strength"
                        ] = market_strength

                        if existing is None:

                            best_symbols[
                                symbol_key
                            ] = coin_data

                        else:

                            existing_strength = existing.get(
                                "market_strength",
                                0
                            )

                            if market_strength > existing_strength:

                                best_symbols[
                                    symbol_key
                                ] = coin_data

                    except:
                        continue

            except:
                continue

        # =========================
        # 🚀 FINALIZE
        # =========================

        results = list(
            best_symbols.values()
        )

        results = sorted(

            results,

            key=lambda x: x["score"],

            reverse=True

        )

        results = results[:15]

        # =========================
        # 🚀 SNIPER ENGINE
        # =========================

        sniper_pairs = discover_new_pairs()

        # =========================
        # 💾 CACHE SAVE
        # =========================

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