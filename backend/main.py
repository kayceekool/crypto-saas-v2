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
    # ⚡ CACHE
    # =========================

    if (
        scanner_cache
        and time.time() - last_update < 20
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
            "moon",
            "alpha",
            "100x",
            "degen",
            "launch",
            "gem",
            "sniper",
            "rocket",
            "agi"
        ]

        results = []

        # =========================
        # 🧠 INSTITUTIONAL DEDUPE ENGINE
        # =========================

        best_symbols = {}

        # =========================
        # 🔍 MAIN LOOP
        # =========================

        for keyword in keywords:

            try:

                response = requests.get(
                    f"https://api.dexscreener.com/latest/dex/search/?q={keyword}",
                    timeout=20,
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

                        chain = str(
                            pair.get("chainId", "")
                        ).lower()

                        if chain != "solana":
                            continue

                        symbol = str(
                            pair.get(
                                "baseToken",
                                {}
                            ).get(
                                "symbol",
                                ""
                            )
                        ).upper()

                        # =========================
                        # 🚫 BAD SYMBOL FILTER
                        # =========================

                        if (
                            len(symbol) < 2
                            or len(symbol) > 12
                        ):
                            continue

                        if symbol in [
                            "USDC",
                            "USDT",
                            "WETH",
                            "WBTC"
                        ]:
                            continue

                        price = float(
                            pair.get(
                                "priceUsd",
                                0
                            ) or 0
                        )

                        change = float(
                            pair.get(
                                "priceChange",
                                {}
                            ).get(
                                "h24",
                                0
                            ) or 0
                        )

                        liquidity = float(
                            pair.get(
                                "liquidity",
                                {}
                            ).get(
                                "usd",
                                0
                            ) or 0
                        )

                        volume = float(
                            pair.get(
                                "volume",
                                {}
                            ).get(
                                "h24",
                                0
                            ) or 0
                        )

                        fdv = float(
                            pair.get(
                                "fdv",
                                0
                            ) or 0
                        )

                        pair_address = pair.get(
                            "pairAddress",
                            ""
                        )

                        pair_created = pair.get(
                            "pairCreatedAt",
                            0
                        )

                        dex_url = (
                            f"https://dexscreener.com/solana/{pair_address}"
                        )

        # =========================
# 🚫 INSTITUTIONAL FILTERS
# =========================

if liquidity < 20000:
    continue

if volume < 1000:
    continue

# avoid fake ghost tokens
if price <= 0:
    continue

# suspicious names
bad_words = [
    "test",
    "fake",
    "scam",
    "rug",
    "honeypot",
    "v2",
    "v3",
    "inuinu",
]

symbol_lower = symbol.lower()

if any(x in symbol_lower for x in bad_words):
    continue

# unrealistic pumps
if change > 5000:
    continue

# insane fake fdv
if fdv > 50000000000:
    continue

if fdv <= 0:
    fdv = liquidity * 10

# =========================
# 🕒 TOKEN AGE
# =========================

age_minutes = 999999

if pair_created:

    age_minutes = (
        time.time() - (
            pair_created / 1000
        )
    ) / 60

age_hours = round(
    age_minutes / 60,
    1
)

# =========================
# 🚀 NEW TOKEN DETECTION
# =========================

if age_minutes <= 360:
    token_type = "NEW"
else:
    token_type = "TRENDING"

# =========================
# 🧠 SMART MOMENTUM ENGINE
# =========================

score = 0

# liquidity quality
if liquidity > 25000:
    score += 20

if liquidity > 100000:
    score += 40

if liquidity > 500000:
    score += 60

# volume quality
if volume > 10000:
    score += 20

if volume > 100000:
    score += 40

if volume > 500000:
    score += 70

# price momentum
if change > 5:
    score += 20

if change > 20:
    score += 40

if change > 100:
    score += 80

# fresh launches
if age_minutes <= 360:
    score += 80

if age_minutes <= 120:
    score += 100

# healthy ratio
volume_liquidity_ratio = volume / liquidity

if volume_liquidity_ratio > 0.3:
    score += 30

if volume_liquidity_ratio > 1:
    score += 50

# fdv sanity
if (
    fdv > liquidity * 3
    and fdv < liquidity * 200
):
    score += 20

# =========================
# 🧠 CONFIDENCE ENGINE
# =========================

confidence = 50

if liquidity > 50000:
    confidence += 10

if volume > 50000:
    confidence += 10

if change > 10:
    confidence += 10

if age_minutes <= 240:
    confidence += 10

if whale_status == "🐋 WHALE BUYING":
    confidence += 10

confidence = min(confidence, 99)
                        # =========================
                        # 🐋 WHALE DETECTION
                        # =========================

                        whale_status = "NONE"

                        if (
                            liquidity > 100000
                            and volume > 100000
                        ):

                            whale_status = "🐋 WHALE BUYING"

                            score += 40

                        # =========================
                        # 🎯 CONFIDENCE
                        # =========================

                        confidence = min(
                            99,
                            max(
                                50,
                                int(score / 5)
                            )
                        )

                        # =========================
                        # 🚨 RATING
                        # =========================

                        if score >= 600:

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
                        # 🛡️ RISK
                        # =========================

                        if liquidity > 100000:
                            risk = "LOW"

                        elif liquidity > 40000:
                            risk = "MEDIUM"

                        else:
                            risk = "HIGH"

                        # =========================
                        # ⚡ JUPITER CHECK
                        # =========================

                        jupiter = get_jupiter_quote()

                        coin_data = {

                            "type": token_type,

                            "name": symbol,

                            "price": round(price, 8),

                            "change": round(change, 2),

                            "liquidity": round(liquidity, 2),

                            "volume": round(volume, 2),

                            "score": score,

                            "rating": rating,

                            "risk": risk,

                            "signal": signal,

                            "confidence": f"{confidence}%",

                            "whales": whale_status,

                            "age": f"{age_hours}h",

                            "url": dex_url,

                            "jupiter": (
                                "ONLINE"
                                if "error" not in jupiter
                                else "OFFLINE"
                            )
                        }

                        # =========================
                        # 🧠 INSTITUTIONAL DEDUPE
                        # =========================

                        symbol_key = symbol.upper()

                        existing = best_symbols.get(
                            symbol_key
                        )

                        market_strength = (
                            liquidity
                            + volume
                            + (score * 1000)
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

                            # keep strongest pair only
                            if (
                                market_strength
                                > existing_strength
                            ):

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

        # remove helper field
        for r in results:

            if "market_strength" in r:
                del r["market_strength"]

        # sort
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # limit
        results = results[:15]

        # sniper engine
        sniper_pairs = discover_new_pairs()

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