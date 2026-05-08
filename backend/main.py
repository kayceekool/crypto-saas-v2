from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    return {
        "status": "HEDGE_FUND_SAAS_RUNNING"
    }

@app.get("/scan")
def scan():

    return [
        {
            "token": "BONK",
            "score": 150,
            "signal": "BUY"
        }
    ]