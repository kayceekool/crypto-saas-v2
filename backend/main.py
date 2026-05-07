from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# ✅ Allow frontend (Vercel) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Cache system (prevents rate-limit + speeds up responses)
cache = []
last_update = 0


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ Return cached data if less than 30s old
    if cache and (time.time() - last_update < 30):
        return JSONResponse(content=cache)

    try:
        # 🔗 CoinGecko API
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "bitcoin,ethereum,binancecoin,solana,xrp,cardano,dogecoin,tron,polygon",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        r = requests.get(url, params=params, timeout=15)

        print("CoinGecko Status Code:", r.status_code)
        print("CoinGecko Response:", r.text)

        # 🚨 If API fails, return last good cache
        if r.status_code != 200:
            return JSONResponse(content=cache if cache else [])

        data = r.json()

        if not isinstance(data, dict):
            return JSONResponse(content=cache if cache else [])

        result = []

        # 🔄 Convert API data into frontend format
        for coin, info in data.items():
            if isinstance(info, dict):
                result.append({
                    "name": coin.upper(),
                    "price": info.get("usd", 0),
                    "change": round(info.get("usd_24h_change", 0), 2)
                })

        # 🚨 If API returns empty data
        if not result:
            return JSONResponse(content=cache if cache else [])

        # 📊 Sort by volatility (big movers first)
        result = sorted(result, key=lambda x: abs(x["change"]), reverse=True)

        # 💾 Save cache
        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        # 🚨 Always return safe response (NEVER STATUS fallback)
        return JSONResponse(content=cache if cache else [])