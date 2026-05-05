import time
import requests
from fastapi import FastAPI

app = FastAPI()

# 🔒 cache (prevents API rate limit issues)
scan_cache = []
scan_last = 0

@app.get("/scan")
def scan_market():
    global scan_cache, scan_last

    # ⏱️ return cached data if within 30 seconds
    if scan_cache and (time.time() - scan_last < 30):
        return scan_cache

    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,xrp,cardano,dogecoin,tron,polygon&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        data = response.json()

        # 🚨 block invalid / rate-limited responses
        if not isinstance(data, dict) or "status" in data:
            return scan_cache

        result = []

        for coin, info in data.items():
            # skip anything invalid
            if not isinstance(info, dict):
                continue

            result.append({
                "name": coin.upper(),
                "price": info.get("usd", 0),
                "change": round(info.get("usd_24h_change", 0), 2)
            })

        # 🚨 if nothing valid came back
        if len(result) == 0:
            return scan_cache

        # 🔥 sort by biggest movers
        result = sorted(result, key=lambda x: abs(x["change"]), reverse=True)

        # 💾 save cache
        scan_cache = result
        scan_last = time.time()

        return result

    except Exception:
        return scan_cache