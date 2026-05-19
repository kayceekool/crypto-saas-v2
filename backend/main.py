# ================================
# 🚀 CRYPTO SCANNER AI ENGINE
# ULTRA SNIPER UPGRADE
# ================================

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

DEX_URL = "https://api.dexscreener.com/latest/dex/search"

SEARCH_TERMS = [
    "ai","degen","wojak","pepe","bonk",
    "pump","cat","dog","100x","moon",
    "launch","alpha","sniper"
]

PUMPFUN_TERMS = [
    "pump",
    "new",
    "launch",
    "moon",
    "meme",
    "dog",
    "cat",
    "ai",
    "pepe",
    "bonk",
    "degen",
    "100x",
    "elon",
    "sol",
    "trump",
    "sniper",
    "gem"
]

momentum_memory = {}
blacklist = set()

# =========================
# FETCH TOKENS
# =========================

def fetch_pairs():

    all_pairs = []

    all_search_terms = (
        SEARCH_TERMS +
        PUMPFUN_TERMS
    )

    for term in all_search_terms:

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

            try:
                data = response.json()

            except:
                continue

            pairs = data.get("pairs", [])

            if isinstance(pairs, list):
                all_pairs.extend(pairs)

        except:
            pass

    return all_pairs

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

            chain = pair.get(
                "chainId",""
            )

            if chain != "solana":
                continue

            symbol = (
                pair.get("baseToken",{})
                .get("symbol","UNKNOWN")
                .upper()
            )

            if symbol in blacklist:
                continue

            pair_address = pair.get(
                "pairAddress",""
            )

            price = float(
                pair.get("priceUsd",0) or 0
            )

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

            txns_data = pair.get(
                "txns",{}
            ).get("h24",{})

            buys = int(
                txns_data.get("buys",0)
            )

            sells = int(
                txns_data.get("sells",0)
            )

            txns = buys + sells

            pair_created = pair.get(
                "pairCreatedAt"
            )

            fdv = float(
                pair.get("fdv",0) or 0
            )

            market_cap = fdv

            age_hours = 999999

            if pair_created:

                age_hours = (
                    now - (
                        pair_created / 1000
                    )
                ) / 3600

            # =========================
            # SMART FILTERS
            # =========================

            if liquidity < 5000:
                continue

            if volume < 50:
                continue

            if txns < 5:
                continue

            if (
                market_cap > 50000000 and
                liquidity < 25000
            ):
                continue

            if (
                market_cap >
                liquidity * 500
            ):
                continue

            if (
                age_hours < 12 and
                volume < 500
            ):
                continue

            # =========================
            # RUG FILTER
            # =========================

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

            score += min(
                liquidity / 1000,
                250
            )

            score += min(
                volume / 1000,
                350
            )

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
                    (
                        liquidity -
                        memory["liquidity"]
                    )
                    / memory["liquidity"]
                ) * 100

            except:
                pass

            try:

                price_growth = (
                    (
                        price -
                        memory["price"]
                    )
                    / memory["price"]
                ) * 100

            except:
                pass

            # =========================
            # TREND AI
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
            # WHALE RATIO
            # =========================

            whale_ratio = 0

            if liquidity > 0:

                whale_ratio = (
                    volume / liquidity
                )

            if whale_ratio > 1:
                score += 120

            if whale_ratio > 2:
                score += 240

            if whale_ratio > 4:
                score += 400

            # =========================
            # HYPE ENGINE
            # =========================

            if (
                age_hours < 24 and
                volume > 50000
            ):
                score += 180

            if (
                age_hours < 12 and
                txns > 300
            ):
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

            if (
                price_change > 80 and
                volume_growth > 50 and
                buys > sells
            ):
                score += 350

            # =========================
            # VOLUME ACCELERATION AI
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
            # ELITE WHALE ENGINE
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
            # BREAKOUT CONTINUATION
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
            # DEAD PAIR FILTER
            # =========================

            dead_pair_penalty = 0

            if volume < 1000:
                dead_pair_penalty += 80

            if txns < 25:
                dead_pair_penalty += 120

            if (
                volume <
                liquidity * 0.01
            ):
                dead_pair_penalty += 180

            if (
                buys < sells and
                price_change < -20
            ):
                dead_pair_penalty += 220

            score -= dead_pair_penalty

            # =========================
            # TREND PERSISTENCE AI
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
            # SCAM DETECTION ENGINE
            # =========================

            scam_score = 0

            if (
                market_cap > 10000000 and
                liquidity < 50000
            ):
                scam_score += 80

            if liquidity > 0:

                mc_liq_ratio = (
                    market_cap / liquidity
                )

                if mc_liq_ratio > 300:
                    scam_score += 60

                if mc_liq_ratio > 800:
                    scam_score += 120

            if (
                age_hours < 3 and
                liquidity > 10000000
            ):
                scam_score += 150

            if (
                txns < 20 and
                volume > 100000
            ):
                scam_score += 120

            if (
                buys > 0 and
                sells > 0
            ):

                buy_sell_ratio = (
                    buys / sells
                )

                if (
                    buy_sell_ratio > 8 or
                    buy_sell_ratio < 0.12
                ):
                    scam_score += 70

            if (
                liquidity <
                (
                    market_cap * 0.002
                )
            ):
                scam_score += 80

            if (
                market_cap > 5000000 and
                volume < 5000
            ):
                scam_score += 120

            score -= scam_score

            # =========================
            # EARLY PUMPFUN SNIPER
            # =========================

            early_launch_bonus = 0

            if age_hours < 6:

                early_launch_bonus += 100

                if volume > 10000:
                    early_launch_bonus += 120

                if txns > 80:
                    early_launch_bonus += 140

                if buys > sells:
                    early_launch_bonus += 120

                if volume_growth > 30:
                    early_launch_bonus += 180

                if liquidity_growth > 15:
                    early_launch_bonus += 160

                if whale_ratio > 1:
                    early_launch_bonus += 140

            if (
                age_hours < 24 and
                price_change > 150 and
                volume > 1000000
            ):
                early_launch_bonus += 500

            score += early_launch_bonus

            # =========================
            # SCORE DECAY
            # =========================

            if age_hours > 2000:
                score *= 0.7

            if age_hours > 8000:
                score *= 0.5

            score = int(score)

            # =========================
            # SIGNAL ENGINE
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
            # RATING ENGINE
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
            # CONFIDENCE ENGINE
            # =========================

            confidence = min(
                99,
                max(
                    50,
                    int(score / 15)
                )
            )

            # =========================
            # RISK ENGINE
            # =========================

            risk = "HIGH"

            if liquidity > 30000:
                risk = "MEDIUM"

            if liquidity > 100000:
                risk = "LOW"

            if scam_score >= 80:
                risk = "HIGH"

            if scam_score >= 150:
                risk = "EXTREME"

            if (
                age_hours < 12 and
                market_cap > 10000000 and
                volume < 10000
            ):
                risk = "EXTREME"

            # =========================
            # WHALES
            # =========================

            whales = "NONE"

            if (
                whale_ratio > 1 and
                liquidity > 50000
            ):
                whales = "🐋 WHALE BUYING"

            if (
                whale_ratio > 2 and
                liquidity > 100000
            ):
                whales = "🐋 SMART MONEY"

            if (
                whale_ratio > 4 and
                liquidity > 250000
            ):
                whales = "🦈 ELITE WHALES"

            # =========================
            # TOKEN TYPE
            # =========================

            token_type = "TRENDING"

            if age_hours < 6:
                token_type = "PUMPFUN NEW"

            elif age_hours < 24:
                token_type = "NEW LAUNCH"

            elif age_hours < 72:
                token_type = "EARLY"

            coin = {
                "type": token_type,
                "symbol": symbol,
                "marketCap": round(
                    market_cap,2
                ),
                "price": round(price,8),
                "priceChange": round(
                    price_change,2
                ),
                "liquidity": round(
                    liquidity,2
                ),
                "volume": round(volume,2),
                "score": score,
                "rating": rating,
                "risk": risk,
                "signal": signal,
                "confidence": confidence,
                "whales": whales,
                "age": f"{round(age_hours,1)}h",
                "url": (
                    f"https://dexscreener.com/"
                    f"solana/{pair_address}"
                )
            }

            strength = (
                score +
                liquidity +
                volume
            )

            existing = best_symbols.get(
                symbol
            )

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

    final_coins = list(
        best_symbols.values()
    )

    final_coins.sort(
        key=lambda x: (
            x["type"] == "PUMPFUN NEW",
            x["score"],
            x["volume"]
        ),
        reverse=True
    )

    final_coins = final_coins[:20]

    return jsonify(final_coins)

# =========================
# START
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )