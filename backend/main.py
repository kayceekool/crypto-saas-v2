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
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        return {
            "status_code": response.status_code,
            "response": response.text
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "error": str(e)
        }