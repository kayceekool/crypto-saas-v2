from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/scan")
def scan():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "bitcoin,ethereum,solana",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        response = requests.get(
            url,
            params=params,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)

        # 🚨 TEMP DEBUG RESPONSE
        return {
            "status_code": response.status_code,
            "raw_response": response.text
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "error": str(e)
        }