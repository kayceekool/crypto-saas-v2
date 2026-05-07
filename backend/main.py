from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💾 Cache
cache = []
last_update = 0


@app.get("/")
def home():
    return {"message": "Crypto scanner backend running"}


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ Use cache for 20 seconds
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:
        symbols = [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "SOLUSDT",
            "XRPUSDT",
            "ADAUSDT",
            "DOGEUSDT",
            "TRXUSDT"
        ]

        result = []

        for symbol in symbols:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"

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

            result.append({
                "name": symbol.replace("USDT", ""),
                "price": round(float(data.get("lastPrice", 0)), 4),
                "change": round(float(data.get("priceChangePercent", 0)), 2)
            })

        # 🚨 fallback if API fails
        if not result:
            return JSONResponse(content=[])

        # 📊 Sort biggest movers first
        result = sorted(
            result,
            key=lambda x: abs(x["change"]),
            reverse=True
        )

        # 💾 Save cache
        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=cache if cache else [])