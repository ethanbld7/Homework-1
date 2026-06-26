import pandas as pd
import mplfinance as mpf
import time
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def get_historical_bars(symbol):
    url = "https://data.alpaca.markets/v2/stocks/bars"

    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY,
        "accept": "application/json"
    }

    params = {
        "symbols": symbol,
        "timeframe": "5Min",
        "start": "2026-05-23T00:00:00Z",
        "end": "2026-06-23T00:00:00Z",
        "limit": 1000,
        "feed": "iex"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    bars = data["bars"][symbol]
    df = pd.DataFrame(bars)
    df["t"] = pd.to_datetime(df["t"])

    return df

df = get_historical_bars("AAPL")

plot_df = df.rename(columns={
    "t": "Date",
    "o": "Open",
    "h": "High",
    "l": "Low",
    "c": "Close",
    "v": "Volume"
})

plot_df = plot_df[["Date", "Open", "High", "Low", "Close", "Volume"]]
plot_df = plot_df.set_index("Date")

mpf.plot(
    plot_df.tail(100),
    type="candle",
    volume=True,
    title="AAPL 5-Minute OHLCV"
)