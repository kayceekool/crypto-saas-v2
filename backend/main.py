# ================================
# 🚀 CRYPTO SCANNER AI ENGINE
# FULL UPGRADED main.py
# Upgrades 11 → 22 Integrated
# ================================

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import random

app = Flask(__name__)
CORS(app)

# =========================
# 🧠 MOMENTUM MEMORY
# =========================

momentum_memory = {}

# =========================
# 🧠 SYMBOL DEDUPE ENGINE
# =========================

best_symbols = {}

# =========================
# 🔥 CONFIG
# =========================

DEX_URL = "https://api.dexscreener.com/latest/dex/search"

SEARCH_TERMS = [
    "ai",
    "degen",
    "wojak",
    "pepe",
    "bonk",
    "pump",
    "cat",
    "dog",
    "100x",
    "moon",
    "launch",
    "alpha",
    "sniper"
]

# =========================
# 🔥 FETCH TOKENS
# =========================

def fetch_pairs():

    all_pairs = []

    for term in SEARCH_TERMS:

        try:

            url = f"{DEX_URL}?q={term}"

            response = requests.get(url, timeout=10)

            data = response.json()

            pairs = data.get("pairs", [])

            all_pairs.extend(pairs)

        except:
            pass

    return all_pairs

# =========================
# 🔥 MAIN SCANNER
# =========================

@app.route("/scan")

def scan():

    global momentum_memory

    pairs = fetch_pairs()

    filtered_coins = []

    best_symbols = {}

    for pair in pairs:

        try:

            chain = pair.get("chainId", "")

            if chain != "solana":
                continue

            symbol = (
                pair.get("baseToken", {})
                .get("symbol", "UNKNOWN")
            )

            symbol = symbol.upper()

            pair_address = pair.get("pairAddress", "")

            price = float(
                pair.get("priceUsd", 0) or 0
            )

            liquidity = float(
                pair.get("liquidity", {})
                .get("usd", 0) or 0
            )

            volume = float(
                pair.get("volume", {})
                .get("h24", 0) or 0
            )

            price_change = float(
                pair.get("priceChange", {})
                .get("h24", 0) or 0
            )

            txns_data = pair.get("txns", {}).get("h24", {})

            buys = int(
                txns_data.get("buys", 0)
            )

            sells = int(
                txns_data.get("sells", 0)
            )

            txns = buys + sells

            pair_created = pair.get("pairCreatedAt")

            age_hours = 999999

            if pair_created:
                age_hours = (
                    time.time() -
                    (pair_created / 1000)
                ) / 3600

            # =========================
            # ☠️ DEAD TOKEN FILTER
            # =========================

            if liquidity < 8000:
                continue

            if volume < 500:
                continue

            if txns < 15:
                continue

            if age_hours > 30000 and volume < 10000:
                continue

            # =========================
            # 🧠 BASE SCORE
            # =========================

            score = 0

            # liquidity

            if liquidity > 20000:
                score += 60

            if liquidity > 100000:
                score += 120

            if liquidity > 500000:
                score += 200

            # volume

            if volume > 10000:
                score += 80

            if volume > 100000:
                score += 160

            if volume > 500000:
                score += 260

            # price movement

            if price_change > 5:
                score += 60

            if price_change > 20:
                score += 140

            if price_change > 50:
                score += 240

            # transactions

            if txns > 50:
                score += 50

            if txns > 200:
                score += 100

            if txns > 500:
                score += 180

            # age boost

            if age_hours < 24:
                score += 140

            elif age_hours < 72:
                score += 80

            # =========================
            # 🧠 MOMENTUM TRACKING
            # =========================

            pair_key = pair_address

            if pair_key not in momentum_memory:

                momentum_memory[pair_key] = {
                    "last_volume": volume,
                    "last_liquidity": liquidity,
                    "last_price": price,
                    "pump_count": 0,
                    "last_seen": time.time()
                }

            history = momentum_memory[pair_key]

            volume_growth = 0
            liquidity_growth = 0
            price_growth = 0

            try:

                if history["last_volume"] > 0:

                    volume_growth = (
                        (volume - history["last_volume"])
                        / history["last_volume"]
                    ) * 100

            except:
                pass

            try:

                if history["last_liquidity"] > 0:

                    liquidity_growth = (
                        (liquidity - history["last_liquidity"])
                        / history["last_liquidity"]
                    ) * 100

            except:
                pass

            try:

                if history["last_price"] > 0:

                    price_growth = (
                        (price - history["last_price"])
                        / history["last_price"]
                    ) * 100

            except:
                pass

            # =========================
            # 🚀 EARLY PUMP DETECTOR
            # =========================

            early_pump_score = 0

            if volume_growth > 50:
                early_pump_score += 120

            if volume_growth > 100:
                early_pump_score += 220

            if liquidity_growth > 20:
                early_pump_score += 100

            if price_growth > 15:
                early_pump_score += 150

            if age_hours < 48:
                early_pump_score += 120

            score += early_pump_score

            # =========================
            # 🐋 SMART MONEY
            # =========================

            smart_money_score = 0

            if volume > liquidity * 2:
                smart_money_score += 140

            if buys > sells:
                smart_money_score += 120

            if txns > 300:
                smart_money_score += 100

            if price_change > 20:
                smart_money_score += 150

            score += smart_money_score

            # =========================
            # 🚫 FAKE PUMP FILTER
            # =========================

            fake_pump = False

            if (
                price_change > 300
                and volume < 20000
            ):
                fake_pump = True

            if (
                liquidity < 15000
                and price_change > 150
            ):
                fake_pump = True

            if fake_pump:
                score -= 300

            # =========================
            # 🔥 CONTINUATION ENGINE
            # =========================

            continuation_score = 0

            if volume_growth > 30 and price_change > 20:
                continuation_score += 120

            if (
                volume_growth > 80
                and liquidity_growth > 10
            ):
                continuation_score += 180

            if buys > sells * 1.5:
                continuation_score += 100

            score += continuation_score

            # =========================
            # 🔥 CONFIDENCE ENGINE
            # =========================

            confidence = 50

            if score > 200:
                confidence = 60

            if score > 350:
                confidence = 70

            if score > 500:
                confidence = 85

            if score > 700:
                confidence = 92

            if score > 900:
                confidence = 99

            if fake_pump:
                confidence -= 25

            confidence = max(
                1,
                min(confidence, 99)
            )

            # =========================
            # 🔥 SIGNAL ENGINE
            # =========================

            signal = "NO"

            if score >= 900:
                signal = "ULTRA SEND"

            elif score >= 700:
                signal = "PARABOLIC"

            elif score >= 450:
                signal = "SNIPER ENTRY"

            elif score >= 200:
                signal = "BUY"

            # =========================
            # 🔥 RATING ENGINE
            # =========================

            rating = "⚠️ RISKY"

            if score >= 100:
                rating = "🚀 GOOD"

            if score >= 200:
                rating = "🔥 HOT"

            if score >= 350:
                rating = "💎 GEM"

            if score >= 700:
                rating = "🚀 PARABOLIC"

            if score >= 900:
                rating = "👑 GOD CANDLE"

            # =========================
            # 🔥 RISK ENGINE
            # =========================

            risk = "HIGH"

            if liquidity > 30000:
                risk = "MEDIUM"

            if liquidity > 100000:
                risk = "LOW"

            # =========================
            # 🐋 WHALE DETECTION
            # =========================

            whales = "NONE"

            if volume > liquidity:
                whales = "🐋 WHALE BUYING"

            if volume > liquidity * 2:
                whales = "🐋 SMART MONEY"

            # =========================
            # 🔥 TOKEN TYPE
            # =========================

            token_type = "TRENDING"

            if age_hours < 24:
                token_type = "NEW"

            # =========================
            # 📦 COIN DATA
            # =========================

            coin_data = {
                "type": token_type,
                "symbol": symbol,
                "price": round(price, 8),
                "priceChange": round(price_change, 2),
                "liquidity": round(liquidity, 2),
                "volume": round(volume, 2),
                "score": int(score),
                "rating": rating,
                "risk": risk,
                "signal": signal,
                "confidence": confidence,
                "whales": whales,
                "age": f"{round(age_hours,1)}h",
                "url": f"https://dexscreener.com/solana/{pair_address}"
            }

            # =========================
            # 🧠 INSTITUTIONAL DEDUPE
            # =========================

            market_strength = (
                liquidity +
                volume +
                (score * 1000)
            )

            coin_data["market_strength"] = market_strength

            existing = best_symbols.get(symbol)

            if existing is None:

                best_symbols[symbol] = coin_data

            else:

                existing_strength = existing.get(
                    "market_strength",
                    0
                )

                if market_strength > existing_strength:

                    best_symbols[symbol] = coin_data

            # =========================
            # 💾 SAVE HISTORY
            # =========================

            momentum_memory[pair_key] = {
                "last_volume": volume,
                "last_liquidity": liquidity,
                "last_price": price,
                "pump_count": (
                    history.get("pump_count", 0) + 1
                ),
                "last_seen": time.time()
            }

        except:
            pass

    # =========================
    # 🔄 FINAL MARKET ROTATION
    # =========================

    filtered_coins = list(best_symbols.values())

    filtered_coins.sort(
        key=lambda x: (
            x.get("score", 0),
            x.get("volume", 0),
            x.get("liquidity", 0)
        ),
        reverse=True
    )

    final_coins = []

    used_symbols = set()

    for coin in filtered_coins:

        sym = coin["symbol"].upper()

        if sym in used_symbols:
            continue

        used_symbols.add(sym)

        final_coins.append(coin)

        if len(final_coins) >= 15:
            break

    filtered_coins = final_coins

    return jsonify(filtered_coins)

# =========================
# 🚀 START SERVER
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )