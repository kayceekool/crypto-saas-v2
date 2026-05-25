# ================================
# 🚀 CRYPTO SCANNER AI ENGINE
# REAL SNIPER ENGINE V4
# Pump.fun Early Detection Upgrade
# Advanced Scam Filtering Upgrade
# ================================

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

DEX_URL = "https://api.dexscreener.com/latest/dex/search"

momentum_memory = {}
blacklist = set()

# =========================
# FETCH PAIRS
# PHASE 1 PUMPFUN SNIPER
# =========================

def fetch_pairs():

    all_pairs = []
    seen_pairs = set()

    sniper_terms = [
        "pump",
        "pumpfun",
        "moon",
        "launch",
        "meme",
        "new",
        "sol",
        "ai",
        "dog",
        "cat",
        "pepe",
        "bonk",
        "wojak",
        "degen",
        "100x",
        "gem",
        "trending",
        "elon",
        "trump",
        "sniper",
        "fresh",
        "early"
    ]

    for term in sniper_terms:

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

            if not isinstance(pairs, list):
                continue

            for pair in pairs:

                try:

                    pair_address = pair.get(
                        "pairAddress",""
                    )

                    if (
                        not pair_address or
                        pair_address in seen_pairs
                    ):
                        continue

                    seen_pairs.add(
                        pair_address
                    )

                    if (
                        pair.get(
                            "chainId",""
                        ) != "solana"
                    ):
                        continue

                    liquidity = float(
                        pair.get(
                            "liquidity",{}
                        ).get("usd",0) or 0
                    )

                    volume = float(
                        pair.get(
                            "volume",{}
                        ).get("h24",0) or 0
                    )

                    txns_data = pair.get(
                        "txns",{}
                    ).get("h24",{})

                    buys = int(
                        txns_data.get(
                            "buys",0
                        )
                    )

                    sells = int(
                        txns_data.get(
                            "sells",0
                        )
                    )

                    txns = buys + sells

                    if liquidity < 3000:
                        continue

                    if volume < 100:
                        continue

                    if txns < 3:
                        continue

                    all_pairs.append(pair)

                except:
                    pass

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
                    now - (pair_created / 1000)
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

            if (
                liquidity < 50000 and
                market_cap > 10000000
            ):
                rug_probability += 40

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
                    "price": price
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
            # WHALE ENGINE
            # =========================

            whale_ratio = 0

            if liquidity > 0:
                whale_ratio = volume / liquidity

            if whale_ratio > 1:
                score += 120

            if whale_ratio > 2:
                score += 240

            if whale_ratio > 4:
                score += 400

            # =========================
            # EARLY LAUNCH SNIPER
            # =========================

            if age_hours < 1:
                score += 400

            elif age_hours < 3:
                score += 250

            elif age_hours < 6:
                score += 120

            # =========================
            # EXTREME EARLY DETECTION
            # =========================

            early_sniper_score = 0

            if age_hours < 0.25:
                early_sniper_score += 600

            elif age_hours < 0.5:
                early_sniper_score += 450

            elif age_hours < 1:
                early_sniper_score += 300

            if sells > 0 and buys > sells * 3:
                early_sniper_score += 220

            if sells > 0 and buys > sells * 5:
                early_sniper_score += 350

            if txns > 50 and age_hours < 1:
                early_sniper_score += 180

            if txns > 120 and age_hours < 1:
                early_sniper_score += 300

            if (
                liquidity > 15000 and
                age_hours < 1
            ):
                early_sniper_score += 220

            if (
                volume_growth > 40 and
                liquidity_growth > 10
            ):
                early_sniper_score += 260

            if (
                whale_ratio > 1.5 and
                age_hours < 3
            ):
                early_sniper_score += 240

            if (
    sells > 0 and
    price_change > 20 and
    buys > sells * 2 and
    txns > 80
):
            ):
                early_sniper_score += 320

            score += early_sniper_score

            # =========================
            # SMART RISK ENGINE V3
            # =========================

            risk = "HIGH"

            if liquidity > 30000:
                risk = "MEDIUM"

            if liquidity > 100000:
                risk = "LOW"

            # =========================
            # OFFICIAL TOKEN DETECTION
            # =========================

            official_like_tokens = [
                "sol",
                "usdc",
                "usdt",
                "btc",
                "eth"
            ]

            meme_impersonation_tokens = [
                "pump",
                "pepe",
                "bonk",
                "wojak",
                "doge",
                "shib",
                "trump",
                "moon",
                "100x",
                "meme",
                "ai"
            ]

            # =========================
            # FAKE MEME CLONE DETECTION
            # =========================

            if (
                symbol.lower() in meme_impersonation_tokens and
                age_hours > 168
            ):
                risk = "EXTREME"

            if (
                symbol.lower() in meme_impersonation_tokens and
                age_hours > 72 and
                volume < 500000
            ):
                risk = "EXTREME"

            if (
                age_hours > 500 and
                volume < liquidity * 0.15
            ):
                risk = "HIGH"

            # =========================
            # MARKET CAP FRAUD
            # =========================

            if (
                market_cap > 100000000 and
                liquidity < 50000
            ):
                risk = "EXTREME"

            if (
                market_cap >
                liquidity * 300
            ):
                risk = "EXTREME"

            # =========================
            # RUG CONDITIONS
            # =========================

            if rug_probability >= 50:
                risk = "EXTREME"

            if (
                age_hours < 6 and
                liquidity < 15000
            ):
                risk = "EXTREME"

            if (
                price_change > 1000 and
                liquidity < 30000
            ):
                risk = "EXTREME"

            # =========================
            # FAKE VOLUME DETECTION
            # =========================

            if (
                volume > liquidity * 20
            ):
                risk = "EXTREME"

            if (
    sells > 0 and
    buys > sells * 20 and
    txns < 80
):
            ):
                risk = "EXTREME"

            # =========================
            # DEAD TOKEN DETECTION
            # =========================

            if (
                age_hours > 2000 and
                volume < 10000
            ):
                risk = "HIGH"

            # =========================
            # SCAM AUTO FILTER
            # =========================

            if risk == "EXTREME":

                blacklist.add(symbol)

                continue

            # =========================
            # CONFIDENCE FORCE CAP
            # =========================

            if risk == "EXTREME":
                confidence_cap = 25

            elif risk == "HIGH":
                confidence_cap = 55

            elif risk == "MEDIUM":
                confidence_cap = 75

            else:
                confidence_cap = 99

            # =========================
            # SIGNAL ENGINE
            # =========================

            signal = "NO"

            if score >= 1700:
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

            if score >= 1600:
                rating = "🧠 AI SUPERNOVA"

            # =========================
            # SMART CONFIDENCE ENGINE
            # =========================

            confidence = 50

            confidence += min(
                int(score / 60),
                25
            )

            if liquidity > 25000:
                confidence += 5

            if liquidity > 100000:
                confidence += 5

            if buys > sells and sells > 0:
                confidence += 5

            if sells > 0 and buys > sells * 2:
                confidence += 5

            if age_hours < 6:
                confidence += 10

            if age_hours < 2:
                confidence += 10

            # =========================
            # SCAM PENALTIES
            # =========================

            if risk == "HIGH":
                confidence -= 35

            if risk == "EXTREME":
                confidence -= 70

            # =========================
            # OLD TOKEN PENALTIES
            # =========================

            if age_hours > 720:
                confidence -= 15

            if age_hours > 3000:
                confidence -= 25

            # =========================
            # LOW ACTIVITY PENALTIES
            # =========================

            if volume < 5000:
                confidence -= 15

            if txns < 25:
                confidence -= 15

            # =========================
            # FINAL RISK CAPS
            # =========================

            confidence = min(
                confidence,
                confidence_cap
            )

            confidence = max(
                5,
                min(confidence,99)
            )

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

            # =========================
            # TOKEN TYPE
            # =========================

            token_type = "TRENDING"

            if age_hours < 0.25:
                token_type = "🚨 STEALTH LAUNCH"

            elif age_hours < 1:
                token_type = "🔥 JUST LAUNCHED"

            elif age_hours < 3:
                token_type = "🚀 NEW PAIR"

            elif age_hours < 6:
                token_type = "⚡ EARLY"

            elif age_hours < 24:
                token_type = "🌱 NEW"

            elif age_hours < 72:
                token_type = "📈 BUILDING"

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
                "score": int(score),
                "rating": rating,
                "risk": risk,
                "signal": signal,
                "confidence": confidence,
                "whales": whales,
                "age": f"{round(age_hours,1)}h",
                "url": (
                    f"https://dexscreener.com/solana/{pair_address}"
                )
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
                "price": price
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
            x["score"],
            x["volume"],
            x["liquidity"]
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