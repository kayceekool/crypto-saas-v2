from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import requests
import time

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
        "status": "ONLINE",
        "scanner": "ACTIVE",
        "ai_engine": "RUNNING"
    }

# =========================
# 🚀 MAIN SCANNER
# =========================

@app.get("/scan")
def scan():

    global scanner_cache
    global sniper_cache
    global last_update

    # =========================
    # ⚡ CACHE STABILIZER
    # =========================

    if scanner_cache and time.time() - last_update < 20:
        return JSONResponse(content={
            "scanner": scanner_cache,
            "new_pairs": sniper_cache
        })

    try:

        keywords = [
            "wojak",
            "pepe",
            "bonk",
            "pump",
            "meme",
            "ai",
            "degen",
            "launch",
            "moon",
            "100x",
            "sniper",
            "alpha",
            "agi"
        ]

        results = []
        best_symbols = {}

        # =========================
        # 🔍 SEARCH LOOP
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

                        # =========================
                        # 🚀 AGE ENGINE
                        # =========================

                        pair_created = pair.get("pairCreatedAt", 0)

                        age_hours = 999999

                        if pair_created:
                            age_hours = (
                                time.time() - (pair_created / 1000)
                            ) / 3600

                        token_type = (
                            "NEW"
                            if age_hours <= 6
                            else "TRENDING"
                        )

                        # =========================
                        # 🚨 BASIC FILTERS
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
                            score += 60

                        if liquidity > 500000:
                            score += 80

                        # volume
                        if volume > 25000:
                            score += 50

                        if volume > 100000:
                            score += 80

                        if volume > 1000000:
                            score += 120

                        # momentum
                        if change > 5:
                            score += 50

                        if change > 20:
                            score += 120

                        if change > 100:
                            score += 250

                        # new token bonus
                        if age_hours <= 6:
                            score += 180

                        if age_hours <= 2:
                            score += 220

                        # fdv sanity
                        if fdv > 1000000:
                            score += 40

                        # =========================
                        # 🚀 VIRALITY ENGINE
                        # =========================

                        virality = "NORMAL"

                        if volume > liquidity:
                            score += 70
                            virality = "TRENDING"

                        if volume > liquidity * 3:
                            score += 150
                            virality = "VIRAL"

                        if volume > liquidity * 8:
                            score += 300
                            virality = "EXPLODING"

                        # =========================
                        # 🐋 SMART MONEY ENGINE
                        # =========================

                        whales = "NONE"

                        if volume > liquidity * 0.8:
                            whales = "🐋 WHALE BUYING"
                            score += 50

                        if volume > liquidity * 2:
                            whales = "🐋 SMART MONEY"
                            score += 120

                        # =========================
                        # 🧠 CONFIDENCE ENGINE
                        # =========================

                        confidence = 50

                        if score > 150:
                            confidence = 70

                        if score > 300:
                            confidence = 85

                        if score > 500:
                            confidence = 99

                        # =========================
                        # ⚡ SIGNAL ENGINE
                        # =========================

                        if score >= 900:
                            rating = "👑 GOD CANDLE"
                            signal = "ULTRA SEND"

                        elif score >= 500:
                            rating = "🚀 PARABOLIC"
                            signal = "PARABOLIC"

                        elif score >= 250:
                            rating = "💎 GEM"
                            signal = "SNIPER ENTRY"

                        elif score >= 150:
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
                        # 🧠 AI ENTRY ENGINE
                        # =========================

                        entry_zone = "WAIT"

                        if score >= 250:
                            entry_zone = "SNIPER ZONE"

                        if score >= 500:
                            entry_zone = "EARLY BREAKOUT"

                        if score >= 900:
                            entry_zone = "FULL SEND"

                        coin_data = {
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
                            "confidence": f"{confidence}%",
                            "whales": whales,
                            "age": f"{round(age_hours, 1)}h",
                            "virality": virality,
                            "entry": entry_zone,
                            "url": dex_url
                        }

                        # =========================
                        # 🧠 INSTITUTIONAL DEDUPE
                        # =========================

                        symbol_key = symbol.upper()

                        market_strength = (
                            liquidity +
                            volume +
                            (score * 1000)
                        )

                        coin_data["market_strength"] = market_strength

                        existing = best_symbols.get(symbol_key)

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
        # 📊 FINALIZE
        # =========================

        results = list(best_symbols.values())

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        results = results[:15]

        scanner_cache = results
        sniper_cache = []

        last_update = time.time()

        return JSONResponse(content={
            "scanner": results,
            "new_pairs": sniper_cache
        })

    except Exception as e:

        return JSONResponse(content={
            "scanner": scanner_cache,
            "new_pairs": sniper_cache,
            "error": str(e)
        })