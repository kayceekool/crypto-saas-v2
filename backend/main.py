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
# 🔥 SMART KEYWORDS
# =========================

keywords = [
    "pump",
    "ai",
    "sniper",
    "launch",
    "degen",
    "moon",
    "alpha",
    "agi",
    "meme",
    "cat",
    "dog",
    "wojak",
    "bonk",
    "pepe",
    "sol"
]

# =========================
# 🏦 ROOT
# =========================

@app.get("/")
def home():

    return {
        "status": "HEDGE_FUND_SAAS_RUNNING",
        "scanner": "ACTIVE",
        "sniper_engine": "ACTIVE",
        "dex": "JUPITER_ENABLED",
        "version": "INSTITUTIONAL_AI_V5"
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
    # ⚡ CACHE SYSTEM
    # =========================

    if scanner_cache and time.time() - last_update < 20:

        return JSONResponse(content={
            "scanner": scanner_cache,
            "new_pairs": sniper_cache,
            "cached": True
        })

    try:

        best_symbols = {}

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

                        chain = pair.get("chainId", "").lower()

                        if chain != "solana":
                            continue

                        base = pair.get("baseToken", {})

                        symbol = base.get("symbol", "UNKNOWN")

                        if not symbol:
                            continue

                        symbol = symbol.upper().strip()

                        # =========================
                        # 🚫 IGNORE BAD SYMBOLS
                        # =========================

                        if len(symbol) > 15:
                            continue

                        if symbol in ["UNKNOWN", "???"]:
                            continue

                        price = float(pair.get("priceUsd", 0) or 0)

                        change = float(
                            pair.get("priceChange", {}).get("h24", 0) or 0
                        )

                        liquidity = float(
                            pair.get("liquidity", {}).get("usd", 0) or 0
                        )

                        volume = float(
                            pair.get("volume", {}).get("h24", 0) or 0
                        )

                        fdv = float(pair.get("fdv", 0) or 0)

                        pair_address = pair.get("pairAddress", "")

                        dex_url = (
                            f"https://dexscreener.com/solana/{pair_address}"
                        )

                        pair_created = pair.get("pairCreatedAt", 0)

                        # =========================
                        # ⏳ AGE ENGINE
                        # =========================

                        age_hours = 999999

                        if pair_created:

                            age_hours = round(
                                (
                                    time.time() - (pair_created / 1000)
                                ) / 3600,
                                1
                            )

                        # =========================
                        # 🚨 MINIMUM FILTERS
                        # =========================

                        if liquidity < 10000:
                            continue

                        if volume < 100:
                            continue

                        # =========================
                        # 🧠 AI SCORE ENGINE
                        # =========================

                        score = 0

                        # liquidity
                        if liquidity > 25000:
                            score += 40

                        if liquidity > 100000:
                            score += 50

                        if liquidity > 500000:
                            score += 60

                        # volume
                        if volume > 10000:
                            score += 40

                        if volume > 100000:
                            score += 60

                        if volume > 500000:
                            score += 80

                        # price momentum
                        if change > 5:
                            score += 40

                        if change > 25:
                            score += 80

                        if change > 100:
                            score += 140

                        if change > 500:
                            score += 240

                        # fdv
                        if fdv > 100000:
                            score += 20

                        if fdv > 1000000:
                            score += 40

                        # young token bonus
                        if age_hours <= 6:
                            score += 120

                        elif age_hours <= 24:
                            score += 80

                        elif age_hours <= 72:
                            score += 40

                        # volume vs liquidity
                        if volume > liquidity:
                            score += 40

                        if volume > liquidity * 2:
                            score += 80

                        # =========================
                        # 🚀 TOKEN TYPE
                        # =========================

                        if age_hours <= 6:
                            token_type = "NEW"
                        else:
                            token_type = "TRENDING"

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
                        # 🚀 SIGNAL ENGINE
                        # =========================

                        if score >= 500:
                            signal = "PARABOLIC"

                        elif score >= 250:
                            signal = "SNIPER ENTRY"

                        elif score >= 150:
                            signal = "BUY"

                        else:
                            signal = "NO"

                        # =========================
                        # 🏆 RATING ENGINE
                        # =========================

                        if score >= 500:
                            rating = "🚀 PARABOLIC"

                        elif score >= 250:
                            rating = "💎 GEM"

                        elif score >= 150:
                            rating = "🔥 HOT"

                        elif score >= 80:
                            rating = "🚀 GOOD"

                        else:
                            rating = "⚠️ RISKY"

                        # =========================
                        # 🐋 WHALE ENGINE
                        # =========================

                        if volume > liquidity * 1.5:
                            whales = "🐋 WHALE BUYING"
                        else:
                            whales = "NONE"

                        # =========================
                        # 📈 CONFIDENCE ENGINE
                        # =========================

                        confidence = 50

                        if score >= 150:
                            confidence = 70

                        if score >= 250:
                            confidence = 85

                        if score >= 400:
                            confidence = 99

                        # =========================
                        # ⚡ JUPITER STATUS
                        # =========================

                        jupiter = get_jupiter_quote()

                        # =========================
                        # 🧠 COIN DATA
                        # =========================

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
                            "whales": whales,
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

                        existing = best_symbols.get(symbol_key)

                        market_strength = (
                            liquidity +
                            volume +
                            (score * 1000)
                        )

                        coin_data["market_strength"] = market_strength

                        # keep only strongest pair
                        if existing is None:

                            best_symbols[symbol_key] = coin_data

                        else:

                            existing_strength = existing.get(
                                "market_strength",
                                0
                            )

                            if market_strength > existing_strength:

                                best_symbols[symbol_key] = coin_data

                    except:
                        continue

            except:
                continue

        # =========================
        # 🚀 FINAL SANITIZED LIST
        # =========================

        results = list(best_symbols.values())

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # keep dashboard clean
        results = results[:15]

        # =========================
        # 🚀 SNIPER ENGINE
        # =========================

        sniper_pairs = discover_new_pairs()

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