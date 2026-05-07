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

    # ⏱️ Cache for 20 seconds
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:
        url = "https://api.coincap.io/v2/assets"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text[:300])

        if response.status_code != 200:
            return JSONResponse(content=[])

        data = response.json()

        assets = data.get("data", [])

        result = []

        for coin in assets[:15]:
            try:
                result.append({
                    "name": coin.get("symbol", "UNKNOWN"),
                    "price": round(float(coin.get("priceUsd", 0)), 4),
                    "change": round(float(coin.get("changePercent24Hr", 0)), 2)
                })
            except:
                continue

        # 🚨 If no valid data
        if not result:
            return JSONResponse(content=[])

        # 📊 Sort by biggest movers
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