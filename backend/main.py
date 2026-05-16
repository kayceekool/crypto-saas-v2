# ================================
# 🚀 CRYPTO SCANNER AI ENGINE
# FULL UPGRADED main.py
# Upgrades 23 → 34 Integrated
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
new_launches_cache = []

# =========================
# FETCH TOKENS (SAFE MODE)
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

            # =========================
            # SAFE STATUS CHECK
            # =========================

            if response.status_code != 200:

                print(
                    f"BAD STATUS {response.status_code}"
                )

                continue

            # =========================
            # SAFE JSON PARSE
            # =========================

            try:

                data = response.json()

            except Exception as json_error:

                print(
                    "JSON ERROR:",
                    json_error
                )

                continue

            pairs = data.get("pairs", [])

            if isinstance(pairs, list):

                all_pairs.extend(pairs)

        except Exception as e:

            print(
                "FETCH ERROR:",
                e
            )

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

                chain = item.get("chainId","")

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
# MAIN SCAN
# =========================

@app.route("/scan")
def scan():

    global momentum_memory

    pairs = fetch_pairs()

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

            rug_probability = 0

            if liquidity < 15000:
                rug_probability += 20

            if sells > buys * 2:
                rug_probability += 30

            if price_change < -70:
                rug_probability += 30

            if volume < liquidity * 0.02:
                rug_probability += 20

            if rug_probability >= 70:
                blacklist.add(symbol)
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
            # AI TREND PERSISTENCE
            # =========================

            if volume_growth > 25:
                score += 180

            if volume_growth > 60:
                score += 280

            if liquidity_growth > 10:
                score += 140

            if liquidity_growth > 30:
                score += 220

            if price_growth > 10:
                score += 120

            if price_growth > 25:
                score += 250

            # =========================
            # WHALE ACCUMULATION
            # =========================

            whales = "NONE"

            if whale_legit:

                if whale_ratio > 1:
                    whales = "🐋 WHALE BUYING"

                if whale_ratio > 2:
                    whales = "🐋 SMART MONEY"

                if whale_ratio > 4:
                    whales = "🦈 ELITE WHALES"

# =========================
            # 🚨 SMART RUG FILTER AI
            # =========================

            rug_score = 0

            # fake insane marketcap
            marketcap = liquidity * 2

            if marketcap > 500000000:
                rug_score += 300

            # suspicious huge liquidity
            if liquidity > 50000000 and volume < 10000:
                rug_score += 250

            # suspicious new launch
            if (
                age_hours < 12 and
                liquidity > 1000000 and
                txns < 50
            ):
                rug_score += 280

            # fake price stability
            if (
                abs(price_change) < 0.5 and
                volume < 5000
            ):
                rug_score += 120

            # fake liquidity wall
            if (
                liquidity > volume * 100
            ):
                rug_score += 180

            # sell pressure
            if sells > buys * 3:
                rug_score += 200

            # suspicious low activity
            if txns < 20 and liquidity > 100000:
                rug_score += 180

            # blacklist obvious rugs
            if rug_score >= 400:
                blacklist.add(symbol)
                continue

            # reduce score heavily
            score -= rug_score

            # =========================
            # 🐋 REAL WHALE DETECTOR
            # =========================

            real_whale_score = 0

            whale_legit = False

            # whales only valid if:
            # high txn count
            # healthy buy pressure
            # strong volume

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

                # remove fake whale signals
                whale_ratio = 0

            score += real_whale_score

            # =========================
            # 🔒 LIQUIDITY SAFETY AI
            # =========================

            liquidity_safety = 0

            if liquidity > 25000:
                liquidity_safety += 80

            if liquidity > 100000:
                liquidity_safety += 120

            if liquidity > 500000:
                liquidity_safety += 180

            # punish weak liquidity
            if liquidity < 15000:
                liquidity_safety -= 180

            score += liquidity_safety

            # =========================
            # 🚀 REAL MOMENTUM ENGINE
            # =========================

            momentum_strength = 0

            if volume_growth > 20:
                momentum_strength += 100

            if volume_growth > 50:
                momentum_strength += 180

            if volume_growth > 100:
                momentum_strength += 260

            if (
                buys > sells and
                liquidity_growth > 5
            ):
                momentum_strength += 120

            score += momentum_strength

            # =========================
            # HYPE ENGINE
            # =========================

            if age_hours < 24 and volume > 50000:
                score += 180

            if age_hours < 12 and txns > 300:
                score += 220

            # =========================
            # LIQUIDITY STABILITY
            # =========================

            liquidity_stability = 100

            if liquidity_growth < -20:
                liquidity_stability -= 50

            if liquidity_growth < -40:
                liquidity_stability -= 80

            if liquidity_stability <= 20:
                score -= 250

            # =========================
            # EXTREME PUMP DETECTOR
            # =========================

            extreme_pump_score = 0

            if (
                price_change > 80
                and volume_growth > 50
                and buys > sells
            ):
                extreme_pump_score += 350

            if volume_growth > 100:
                extreme_pump_score += 180

            if volume_growth > 250:
                extreme_pump_score += 320

            if liquidity_growth > 30:
                extreme_pump_score += 160

            if liquidity_growth > 80:
                extreme_pump_score += 260

            if price_growth > 25:
                extreme_pump_score += 180

            if price_growth > 60:
                extreme_pump_score += 320

            score += extreme_pump_score

            # =========================
            # 🚀 VOLUME ACCELERATION AI
            # =========================

            acceleration_score = 0

            if volume_growth > 15:
                acceleration_score += 80

            if volume_growth > 40:
                acceleration_score += 160

            if volume_growth > 80:
                acceleration_score += 260

            if volume_growth > 150:
                acceleration_score += 400

            score += acceleration_score

            # =========================
            # 🐋 ELITE WHALE ENGINE
            # =========================

            elite_whale_score = 0

            buy_pressure = 0

            if sells > 0:
                buy_pressure = buys / sells

            if buy_pressure > 1.2:
                elite_whale_score += 80

            if buy_pressure > 1.8:
                elite_whale_score += 180

            if buy_pressure > 2.5:
                elite_whale_score += 320

            if whale_ratio > 3:
                elite_whale_score += 260

            score += elite_whale_score

            # =========================
            # 🔥 BREAKOUT CONTINUATION
            # =========================

            continuation_score = 0

            if (
                volume_growth > 25 and
                price_change > 10
            ):
                continuation_score += 120

            if (
                volume_growth > 50 and
                liquidity_growth > 10
            ):
                continuation_score += 180

            if (
                buys > sells and
                txns > 200
            ):
                continuation_score += 140

            score += continuation_score

            # =========================
            # ☠️ DEAD PAIR FILTER
            # =========================

            dead_pair_penalty = 0

            if volume < 1000:
                dead_pair_penalty += 80

            if txns < 25:
                dead_pair_penalty += 120

            if (
                volume < liquidity * 0.01
            ):
                dead_pair_penalty += 180

            if (
                buys < sells and
                price_change < -20
            ):
                dead_pair_penalty += 220

            score -= dead_pair_penalty

            # =========================
            # 🧠 TREND PERSISTENCE AI
            # =========================

            persistence_bonus = 0

            if (
                volume_growth > 20 and
                liquidity_growth > 5
            ):
                persistence_bonus += 140

            if (
                whale_ratio > 1.5 and
                buys > sells
            ):
                persistence_bonus += 160

            score += persistence_bonus

            # =========================
            # SCORE DECAY
            # =========================

            if age_hours > 2000:
                score *= 0.7

            if age_hours > 8000:
                score *= 0.5

            score = int(score)

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

            if whale_ratio > 1:
                whales = "🐋 WHALE BUYING"

            if whale_ratio > 2:
                whales = "🐋 SMART MONEY"

            if whale_ratio > 4:
                whales = "🦈 ELITE WHALES"

            token_type = "TRENDING"

            if age_hours < 24:
                token_type = "NEW"

            coin = {
                "type": token_type,
                "symbol": symbol,
                "price": round(price,8),
                "priceChange": round(price_change,2),
                "liquidity": round(liquidity,2),
                "volume": round(volume,2),
                "score": score,
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

        except Exception as e:

            print(
                "SCAN ERROR:",
                e
            )

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