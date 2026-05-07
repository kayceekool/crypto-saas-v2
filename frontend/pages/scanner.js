from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = []
last_update = 0


@app.get("/scan")
def scan():
    global cache, last_update

    # return cache if fresh
    if cache and time.time() - last_update < 30:
        return JSONResponse(content=cache)

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,binancecoin,solana,xrp,cardano,dogecoin,tron,polygon",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        r = requests.get(url, params=params, timeout=10)

        print("CoinGecko status:", r.status_code)
        print("CoinGecko response:", r.text)

        data = r.json()

        if not isinstance(data, dict):
            return JSONResponse(content=cache if cache else [
                {"name": "ERROR", "price": 0, "change": 0}
            ])

        result = []

        for coin, info in data.items():
            if isinstance(info, dict):
                result.append({
                    "name": coin.upper(),
                    "price": info.get("usd", 0),
                    "change": round(info.get("usd_24h_change", 0), 2)
                })

        # IMPORTANT: never return fake STATUS object
        if not result:
            return JSONResponse(content=[
                {"name": "NO DATA", "price": 0, "change": 0}
            ])

        result = sorted(result, key=lambda x: abs(x["change"]), reverse=True)

        cache = result
        last_update = time.time()

        return JSONResponse(content=result)

    except Exception as e:
        print("SCAN ERROR:", str(e))

        return JSONResponse(content=[
            {"name": "ERROR", "price": 0, "change": 0}
        ])