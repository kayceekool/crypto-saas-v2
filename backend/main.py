import time

scan_cache = None
scan_last = 0

@app.get("/scan")
def scan_market():
    global scan_cache, scan_last

    # ✅ Cache for 30 seconds (prevents rate limit)
    if scan_cache and (time.time() - scan_last < 30):
        return scan_cache

    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,xrp,cardano,dogecoin,tron,polygon&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        data = response.json()

        # 🚨 Handle API rate limit or bad response
        if not isinstance(data, dict) or "status" in data:
            return scan_cache if scan_cache else []

        result = []

        for coin, info in data.items():
            result.append({
                "name": coin.upper(),
                "price": info.get("usd", 0),
                "change": round(info.get("usd_24h_change", 0), 2)
            })

        # 🔥 Sort by biggest movers
        result = sorted(result, key=lambda x: abs(x["change"]), reverse=True)

        # ✅ Save cache
        scan_cache = result
        scan_last = time.time()

        return result

    except Exception:
        # ✅ Return last good data if error
        return scan_cache if scan_cache else []