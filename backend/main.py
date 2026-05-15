# =========================================
# 🚀 CRYPTO SCANNER AI ENGINE
# FULL ELITE UPGRADE v33
# =========================================

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import random
import threading

app = Flask(__name__)
CORS(app)

# =========================================
# 🧠 GLOBAL MEMORY
# =========================================

momentum_memory = {}

market_cache = {
    "tokens": [],
    "last_update": 0
}

# =========================================
# 🔥 CONFIG
# =========================================

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
    "sniper",
    "sol",
    "meme",
    "gork",
    "agi"
]

REFRESH_INTERVAL = 20

# =========================================
# 🧠 FETCH TOKENS
# =========================================

def fetch_pairs():

    all_pairs = []

    for term in SEARCH_TERMS:

        try:

            url = f"{DEX_URL}?q={term}"

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            pairs = data.get("pairs", [])

            all_pairs.extend(pairs)

        except:
            pass

    return all_pairs

# =========================================
# 🔥 SCORING ENGINE
# =========================================

def process_market():

    global momentum_memory
    global market_cache

    pairs = fetch_pairs()

    best_symbols = {}

    for pair in pairs:

        try:

            chain = pair.get("chainId", "")

            if chain != "solana":
                continue

            symbol = (
                pair.get("baseToken", {})
                .get("symbol", "UNKNOWN")
            ).upper()

            pair_address = pair.get(
                "pairAddress",
                ""
            )

            if not pair_address:
                continue

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

            txns_data = pair.get(
                "txns",
                {}
            ).get("h24", {})

            buys = int(
                txns_data.get("buys", 0)
            )

            sells = int(
                txns_data.get("sells", 0)
            )

            txns = buys + sells

            pair_created = pair.get(
                "pairCreatedAt"
            )

            age_hours = 999999

            if pair_created:

                age_hours = (
                    time.time() -
                    (pair_created / 1000)
                ) / 3600

            # =========================================
            # 🚫 ELITE FILTERS
            # =========================================

            if liquidity < 10000:
                continue

            if volume < 100:
                continue

            if txns < 10:
                continue

            if age_hours > 40000:
                continue

            if symbol in [
                "USDC",
                "USDT",
                "WETH",
                "WBTC"
            ]:
                continue

            # =========================================
            # 🧠 BASE SCORE
            # =========================================

            score = 0

            # liquidity

            if liquidity > 20000:
                score += 60

            if liquidity > 100000:
                score += 140

            if liquidity > 500000:
                score += 240

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
                score += 260

            # txns

            if txns > 50:
                score += 60

            if txns > 200:
                score += 140

            if txns > 500:
                score += 220

            # age boost

            if age_hours < 24:
                score += 180

            elif age_hours < 72:
                score += 100

            # =========================================
            # 🧠 MOMENTUM MEMORY
            # =========================================

            if pair_address not in momentum_memory:

                momentum_memory[pair_address] = {
                    "last_volume": volume,
                    "last_liquidity": liquidity,
                    "last_price": price
                }

            history = momentum_memory[pair_address]

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

            # =========================================
            # 🚀 PUMP ENGINE
            # =========================================

            if volume_growth > 40:
                score += 120

            if volume_growth > 100:
                score += 240

            if liquidity_growth > 20:
                score += 140

            if price_growth > 15:
                score += 160

            # =========================================
            # 🐋 SMART MONEY
            # =========================================

            if volume > liquidity:
                score += 120

            if volume > liquidity * 2:
                score += 200

            if buys > sells:
                score += 120

            if buys > sells * 2:
                score += 200

            # =========================================
            # 🚫 FAKE PUMP FILTER
            # =========================================

            fake_pump = False

            if (
                price_change > 300 and
                liquidity < 20000
            ):
                fake_pump = True

            if (
                volume < 5000 and
                price_change > 120
            ):
                fake_pump = True

            if fake_pump:
                score -= 400

            # =========================================
            # 🧠 CONFIDENCE
            # =========================================

            confidence = 50

            if score > 200:
                confidence = 65

            if score > 400:
                confidence = 78

            if score > 600:
                confidence = 90

            if score > 850:
                confidence = 99

            # =========================================
            # 🔥 SIGNAL ENGINE
            # =========================================

            signal = "NO"

            if score >= 900:
                signal = "ULTRA SEND"

            elif score >= 650:
                signal = "PARABOLIC"

            elif score >= 350:
                signal = "SNIPER ENTRY"

            elif score >= 180:
                signal = "BUY"

            # =========================================
            # 🔥 RATING
            # =========================================

            rating = "⚠️ RISKY"

            if score >= 100:
                rating = "🚀 GOOD"

            if score >= 180:
                rating = "🔥 HOT"

            if score >= 350:
                rating = "💎 GEM"

            if score >= 650:
                rating = "🚀 PARABOLIC"

            if score >= 900:
                rating = "👑 GOD CANDLE"

            # =========================================
            # 🔥 RISK
            # =========================================

            risk = "HIGH"

            if liquidity > 30000:
                risk = "MEDIUM"

            if liquidity > 100000:
                risk = "LOW"

            # =========================================
            # 🐋 WHALES
            # =========================================

            whales = "NONE"

            if volume > liquidity:
                whales = "🐋 WHALE BUYING"

            if volume > liquidity * 2:
                whales = "🐋 SMART MONEY"

            # =========================================
            # 🏷️ TOKEN TYPE
            # =========================================

            token_type = "TRENDING"

            if age_hours < 24:
                token_type = "NEW"

            # =========================================
            # 📦 DATA
            # =========================================

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

            # =========================================
            # 🧠 INSTITUTIONAL DEDUPE
            # =========================================

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

                if (
                    market_strength >
                    existing.get(
                        "market_strength",
                        0
                    )
                ):

                    best_symbols[symbol] = coin_data

            # =========================================
            # 💾 SAVE MEMORY
            # =========================================

            momentum_memory[pair_address] = {
                "last_volume": volume,
                "last_liquidity": liquidity,
                "last_price": price
            }

        except:
            pass

    # =========================================
    # 🔥 FINAL SORT
    # =========================================

    final_tokens = list(
        best_symbols.values()
    )

    final_tokens.sort(
        key=lambda x: (
            x["score"],
            x["volume"],
            x["liquidity"]
        ),
        reverse=True
    )

    final_tokens = final_tokens[:15]

    market_cache["tokens"] = final_tokens
    market_cache["last_update"] = time.time()

# =========================================
# 🔄 BACKGROUND REFRESH
# =========================================

def background_worker():

    while True:

        try:

            process_market()

        except:
            pass

        time.sleep(REFRESH_INTERVAL)

threading.Thread(
    target=background_worker,
    daemon=True
).start()

# =========================================
# 🌐 API
# =========================================

@app.route("/scan")

def scan():

    return jsonify(
        market_cache["tokens"]
    )

# =========================================
# 🚀 START
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )