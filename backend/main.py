from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.get("/prices")
def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin&vs_currencies=usd"
    data = requests.get(url).json()
    return data

import time

scan_cache = None
scan_last = 0

@app.get("/scan")
def scan_market():
    global scan_cache, scan_last

    # cache 20 seconds
    if scan_cache and (time.time() - scan_last < 20):
        return scan_cache

    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,xrp,cardano,dogecoin,tron,polygon&vs_currencies=usd&include_24hr_change=true"
        data = requests.get(url, timeout=10).json()

        result = []

        for coin, info in data.items():
            result.append({
                "name": coin.upper(),
                "price": info.get("usd", 0),
                "change": round(info.get("usd_24h_change", 0), 2)
            })

        # sort by biggest movers
        result = sorted(result, key=lambda x: abs(x["change"]), reverse=True)

        scan_cache = result
        scan_last = time.time()

        return result

    except Exception as e:
        return {"error": str(e)}