import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://data.alpaca.markets/v2/stocks/bars"

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

headers = {
    "APCA-API-KEY-ID": api_key.strip(),
    "APCA-API-SECRET-KEY": secret_key.strip(),
    "accept": "application/json"
}

params = {
    "symbols": "AAPL",
    "timeframe": "5Min",
    "start": "2026-05-25T00:00:00Z",
    "end": "2026-06-23T00:00:00Z",
    "limit": 1000,
    "feed": "iex"
}

response = requests.get(url, headers=headers, params=params)

print("Status:", response.status_code)
print(response.text)