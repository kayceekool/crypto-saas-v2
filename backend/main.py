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

cache = []
last_update = 0


@app.get("/")
def home():
    return {"message": "Dex scanner backend running"}


@app.get("/scan")
def scan():
    global cache, last_update

    # ⏱️ cache for 20 seconds
    if cache and (time.time() - last_update < 20):
        return JSONResponse(content=cache)

    try:
        url = "https://api.dexscreener.com/latest/dex/search/?q=SOL"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            return JSONResponse(content=[])

        data = response.json()

        pairs = data.get("pairs", [])

        result = []

        for pair in pairs[:15]:
            try:
                result.append({
                    "name": pair["baseToken"]["symbol"],
                    "price": round(float(pair.get("priceUsd", 0)), 6),
                    "change": round(
                        float(pair.get("priceChange", {}).get("h24", 0)),
                        2
                    )
                })
            except:
                continue

        if not result:
            return JSONResponse(content=[])

        # 🔥 biggest movers first
        result = sorted(
            result,
            key=lambda x: abs(x["change"]),
            reverse=True
        )

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=cache if cache else [])