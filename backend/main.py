# ================================
# 🚀 CRYPTO SCANNER AI ENGINE
# FULL UPGRADED main.py
# REAL PUMP.FUN LAUNCH ENGINE
# ================================

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import math
import threading

app = Flask(__name__)
CORS(app)

DEX_URL = "https://api.dexscreener.com/latest/dex/search"

SEARCH_TERMS = [
    "ai","degen","wojak","pepe","bonk",
    "pump","cat","dog","100x","moon",
    "launch","alpha","sniper"
]

momentum_memory = {}
blacklist = set()

# =========================
# 🚀 NEW LAUNCH CACHE
# =========================

new_launches_cache = []

# =========================
# FETCH TOKENS
# =========================

def fetch_pairs():

    all_pairs = []

    for term in SEARCH_TERMS:

        try:

            url = f"{DEX_URL}?q={term}"

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                continue

            data = response.json()

            pairs = data.get("pairs", [])

            if isinstance(pairs, list):
                all_pairs.extend(pairs)

        except:
            pass

    return all_pairs

# =========================
# 🚀 REAL NEW LAUNCH FETCHER
# =========================

def fetch_new_launches():

    global new_launches_cache

    try:

        url = (
            "https://api.dexscreener.com/"
            "token-profiles/latest/v1"
        )

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code != 200:
            return

        data = response.json()

        if not isinstance(data, list):
            return

        fresh_pairs = []

        for item in data:

            try:

                chain = item.get("chainId", "")

                if chain != "solana":
                    continue

                token_address = item.get(
                    "tokenAddress",
                    ""
                )

                if not token_address:
                    continue

                pair_data_url = (
                    f"https://api.dexscreener.com/"
                    f"latest/dex/tokens/"
                    f"{token_address}"
                )

                pair_response = requests.get(
                    pair_data_url,
                    timeout=10
                )

                if pair_response.status_code != 200:
                    continue

                pair_json = pair_response.json()

                pairs = pair_json.get("pairs", [])

                if not pairs:
                    continue

                fresh_pairs.extend(pairs)

            except:
                pass

        new_launches_cache = fresh_pairs[:80]

        print(
            f"Fetched {len(new_launches_cache)} "
            f"fresh launches"
        )

    except Exception as e:

        print(
            "NEW LAUNCH ERROR:",
            e
        )

# =========================
# 🔄 BACKGROUND LAUNCH LOOP
# =========================

def background_launch_fetcher():

    while True:

        try:

            fetch_new_launches()

        except:
            pass

        time.sleep(90)

threading.Thread(
    target=background_launch_fetcher,
    daemon=True
).start()

# =========================
# MAIN SCAN
# =========================

@app.route("/scan")
def scan():

    global momentum_memory

    pairs = fetch_pairs()

    # merge real fresh launches
    pairs.extend(new_launches_cache)

    best_symbols = {}

    now = time.time()

    for pair in pairs:

        try:

            chain = pair.get("chainId","")

            if chain != "solana":
                continue

            symbol = (
                pair.get("baseToken",{})
                .get("symbol","UNKNOWN")
                .upper()
            )

            if symbol in blacklist:
                continue

            pair_address = pair.get("pairAddress","")

            price = float(pair.get("priceUsd",0) or 0)

            liquidity = float(
                pair.get("liquidity",{})
                .get("usd",0) or 0
            )

            volume = float(
                pair.get("volume",{})
                .get("h24",0) or 0
            )

            price_change = float(
                pair.get("priceChange",{})
                .get("h24",0) or 0
            )

            txns_data = pair.get("txns",{}).get("h24",{})

            buys = int(txns_data.get("buys",0))
            sells = int(txns_data.get("sells",0))

            txns = buys + sells

            pair_created = pair.get("pairCreatedAt")

            age_hours = 999999

            if pair_created:

                age_hours = (
                    now - (pair_created / 1000)
                ) / 3600

            # =========================
            # HARD FILTERS
            # =========================

            if liquidity < 10000:
                continue

            if volume < 100:
                continue

            if txns < 10:
                continue

            # =========================
            # BASE SCORE
            # =========================

            score = 0

            score += min(liquidity / 1000, 250)
            score += min(volume / 1000, 350)

            if txns > 50:
                score += 50

            if txns > 200:
                score += 120

            if txns > 500:
                score += 220

            # =========================
            # MOMENTUM MEMORY
            # =========================

            key = pair_address

            if key not in momentum_memory:

                momentum_memory[key] = {
                    "volume": volume,
                    "liquidity": liquidity,
                    "price": price,
                    "score": 0,
                    "seen": now
                }

            memory = momentum_memory[key]

            volume_growth = 0
            liquidity_growth = 0
            price_growth = 0

            try:
                volume_growth = (
                    (volume - memory["volume"])
                    / memory["volume"]
                ) * 100
            except:
                pass

            try:
                liquidity_growth = (
                    (liquidity - memory["liquidity"])
                    / memory["liquidity"]
                ) * 100
            except:
                pass

            try:
                price_growth = (
                    (price - memory["price"])
                    / memory["price"]
                ) * 100
            except:
                pass

            # =========================
            # WHALE RATIO
            # =========================

            whale_ratio = 0

            if liquidity > 0:
                whale_ratio = volume / liquidity

            # =========================
            # 🚨 SMART RUG FILTER AI
            # =========================

            rug_score = 0

            marketcap = liquidity * 2

            if marketcap > 500000000:
                rug_score += 300

            if liquidity > 50000000 and volume < 10000:
                rug_score += 250

            if (
                age_hours < 12 and
                liquidity > 1000000 and
                txns < 50
            ):
                rug_score += 280

            if (
                abs(price_change) < 0.5 and
                volume < 5000
            ):
                rug_score += 120

            if liquidity > volume * 100:
                rug_score += 180

            if sells > buys * 3:
                rug_score += 200

            if txns < 20 and liquidity > 100000:
                rug_score += 180

            if rug_score >= 400:
                blacklist.add(symbol)
                continue

            score -= rug_score

            # =========================
            # 🐋 REAL WHALE DETECTOR
            # =========================

            real_whale_score = 0

            whale_legit = False

            if (
                txns > 150 and
                buys > sells and
                volume > 50000
            ):
                whale_legit = True

            if whale_legit:

                if whale_ratio > 1:
                    real_whale_score += 120

                if whale_ratio > 2:
                    real_whale_score += 240

                if whale_ratio > 4:
                    real_whale_score += 400

            else:
                whale_ratio = 0

            score += real_whale_score

            # =========================
            # 🚀 PUMP.FUN EARLY DETECTOR
            # =========================

            if (
                age_hours < 6 and
                volume > 15000 and
                buys > sells and
                txns > 80
            ):
                score += 280

            if (
                age_hours < 3 and
                liquidity > 20000 and
                volume_growth > 20
            ):
                score += 340

            # =========================
            # TOKEN TYPE
            # =========================

            token_type = "TRENDING"

            if age_hours < 24:
                token_type = "NEW"

            if age_hours < 3:
                token_type = "JUST LAUNCHED"
                score += 320

            if age_hours < 1:
                score += 450

            # =========================
            # SIGNAL
            # =========================

            signal = "NO"

            if score >= 2200:
                signal = "APEX LEGEND"

            elif score >= 1700:
                signal = "SUPERNOVA"

            elif score >= 1200:
                signal = "MEGA BREAKOUT"

            elif score >= 900:
                signal = "ULTRA SEND"

            elif score >= 700:
                signal = "PARABOLIC"

            elif score >= 450:
                signal = "SNIPER ENTRY"

            elif score >= 200:
                signal = "BUY"

            # =========================
            # RATING
            # =========================

            rating = "⚠️ RISKY"

            if score >= 150:
                rating = "🚀 GOOD"

            if score >= 300:
                rating = "🔥 HOT"

            if score >= 500:
                rating = "💎 GEM"

            if score >= 800:
                rating = "🚀 PARABOLIC"

            if score >= 1100:
                rating = "👑 GOD CANDLE"

            if score >= 1400:
                rating = "🌋 NUCLEAR"

            if score >= 1800:
                rating = "🧠 AI SUPERNOVA"

            if score >= 2300:
                rating = "👑 KING SLAYER"

            # =========================
            # CONFIDENCE
            # =========================

            confidence = min(
                99,
                max(50, int(score / 15))
            )

            # =========================
            # RISK
            # =========================

            risk = "HIGH"

            if liquidity > 30000:
                risk = "MEDIUM"

            if liquidity > 100000:
                risk = "LOW"

            # =========================
            # WHALES
            # =========================

            whales = "NONE"

            if whale_legit:

                if whale_ratio > 1:
                    whales = "🐋 WHALE BUYING"

                if whale_ratio > 2:
                    whales = "🐋 SMART MONEY"

                if whale_ratio > 4:
                    whales = "🦈 ELITE WHALES"

            coin = {
                "type": token_type,
                "symbol": symbol,
                "price": round(price,8),
                "priceChange": round(price_change,2),
                "liquidity": round(liquidity,2),
                "volume": round(volume,2),
                "score": int(score),
                "rating": rating,
                "risk": risk,
                "signal": signal,
                "confidence": confidence,
                "whales": whales,
                "age": f"{round(age_hours,1)}h",
                "url": f"https://dexscreener.com/solana/{pair_address}"
            }

            strength = (
                score +
                liquidity +
                volume
            )

            existing = best_symbols.get(symbol)

            if (
                existing is None or
                strength >
                existing["score"] +
                existing["liquidity"] +
                existing["volume"]
            ):
                best_symbols[symbol] = coin

            momentum_memory[key] = {
                "volume": volume,
                "liquidity": liquidity,
                "price": price,
                "score": score,
                "seen": now
            }

        except:
            pass

    final_coins = list(best_symbols.values())

    final_coins.sort(
        key=lambda x: (
            x["score"],
            x["volume"]
        ),
        reverse=True
    )

    final_coins = final_coins[:15]

    return jsonify(final_coins)

# =========================
# START
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )