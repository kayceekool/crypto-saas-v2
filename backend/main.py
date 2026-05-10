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

        "status": "LIVE",

        "engine": "INSTITUTIONAL_SNIPER_AI",

        "scanner": "ACTIVE",

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
    # ⚡ CACHE RETURN
    # =========================

    if (
        scanner_cache
        and time.time() - last_update < 15
    ):

        return JSONResponse(content={

            "scanner": scanner_cache,

            "new_pairs": sniper_cache,

            "cached": True

        })

    try:

        keywords = [

            "pump",
            "ai",
            "meme",
            "sol",
            "cat",
            "dog",
            "wojak",
            "bonk",
            "pepe",
            "moon",
            "gem",
            "launch"

        ]

        results = []

        added_addresses = set()

        added_symbols = set()

        # =========================
        # 🔍 MAIN LOOP
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

                        symbol = pair["baseToken"]["symbol"]

                        symbol_upper = symbol.upper()

                        # =========================
                        # 🚫 DUPLICATE SYMBOL FILTER
                        # =========================

                        if symbol_upper in added_symbols:
                            continue

                        # =========================
                        # 🚫 MAJOR TOKEN FILTER
                        # =========================

                        banned_new = [

                            "BTC",
                            "ETH",
                            "SOL",
                            "USDT",
                            "USDC",
                            "DOGE",
                            "SHIB",
                            "WIF"

                        ]

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

                        buys = float(
                            pair.get(
                                "txns",
                                {}
                            ).get(
                                "h24",
                                {}
                            ).get("buys", 0)
                        )

                        sells = float(
                            pair.get(
                                "txns",
                                {}
                            ).get(
                                "h24",
                                {}
                            ).get("sells", 0)
                        )

                        fdv = float(
                            pair.get("fdv", 0)
                        )

                        # =========================
                        # 🚨 LIQUIDITY FILTER
                        # =========================

                        if liquidity < 15000:
                            continue

                        # =========================
                        # 🚨 DEAD TOKEN FILTER
                        # =========================

                        if volume < 1000:
                            continue

                        if buys <= 0:
                            continue

                        # =========================
                        # 🚀 NEW TOKEN DETECTION
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

                        if (
                            age_minutes <= 360
                            and symbol_upper not in banned_new
                        ):

                            token_type = "NEW"

                        else:

                            token_type = "TRENDING"

                        # =========================
                        # 🧠 AI SCORE
                        # =========================

                        score = 0

                        # liquidity
                        if liquidity > 50000:
                            score += 30

                        if liquidity > 150000:
                            score += 30

                        # volume
                        if volume > 25000:
                            score += 30

                        if volume > 100000:
                            score += 30

                        # momentum
                        if change > 5:
                            score += 20

                        if change > 20:
                            score += 20

                        # fdv
                        if fdv > 1000000:
                            score += 20

                        # whale flow
                        if buys > sells * 2:
                            score += 20

                        # =========================
                        # 🚀 MOMENTUM ACCELERATION
                        # =========================

                        if volume > liquidity:
                            score += 20

                        if change > 30:
                            score += 30

                        if buys > sells * 3:
                            score += 30

                        # =========================
                        # 🚀 FRESH LAUNCH BONUS
                        # =========================

                        if token_type == "NEW":
                            score += 40

                        # =========================
                        # 🚀 ULTRA EARLY SNIPER
                        # =========================

                        if age_minutes <= 30:
                            score += 60

                        elif age_minutes <= 120:
                            score += 40

                        elif age_minutes <= 360:
                            score += 20

                        # =========================
                        # 🚨 RATING
                        # =========================

                        if score >= 220:
                            rating = "🚨 GOD MODE"

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
                        # 🛡️ RISK
                        # =========================

                        if liquidity > 100000:
                            risk = "LOW"

                        elif liquidity > 40000:
                            risk = "MEDIUM"

                        else:
                            risk = "HIGH"

                        # =========================
                        # 📡 SIGNAL
                        # =========================

                        if score >= 220:
                            signal = "NUCLEAR BUY"

                        elif score >= 180:
                            signal = "STRONG BUY"

                        elif score >= 120:
                            signal = "BUY"

                        else:
                            signal = "NO"

                        # =========================
                        # 🔗 URL
                        # =========================

                        dex_url = (
                            f"https://dexscreener.com/solana/{pair_address}"
                        )

                        # =========================
                        # ⚡ JUPITER
                        # =========================

                        jupiter = get_jupiter_quote()

                        added_addresses.add(pair_address)

                        added_symbols.add(symbol_upper)

                        results.append({

                            "type": token_type,

                            "name": symbol_upper,

                            "price": round(price, 8),

                            "change": round(change, 2),

                            "liquidity": round(liquidity, 2),

                            "volume": round(volume, 2),

                            "score": score,

                            "rating": rating,

                            "risk": risk,

                            "signal": signal,

                            "url": dex_url,

                            "buys": buys,

                            "sells": sells,

                            "age_minutes": round(age_minutes, 1),

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
        # 📊 INSTITUTIONAL SORT
        # =========================

        results = sorted(

            results,

            key=lambda x: (

                x["score"],

                x["volume"],

                x["liquidity"],

                x["change"]

            ),

            reverse=True
        )

        # =========================
        # 🚀 LIMIT
        # =========================

        results = results[:25]

        scanner_cache = results

        sniper_cache = sniper_pairs

        last_update = time.time()

        return JSONResponse(content={

            "scanner": results,

            "new_pairs": sniper_pairs,

            "cached": False

        })

    except Exception as e:

        print("SCAN ERROR:", str(e))

        return JSONResponse(content={

            "scanner": scanner_cache,

            "new_pairs": sniper_cache,

            "error": str(e)

        })