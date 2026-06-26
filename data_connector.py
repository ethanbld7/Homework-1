import os
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd
import mplfinance as mpf
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

BASE_URL = "https://data.alpaca.markets/v2"


def get_headers():
    return {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY,
        "accept": "application/json"
    }


def get_historical_bars(symbol):
    symbol = symbol.upper().strip()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=35)

    url = f"{BASE_URL}/stocks/bars"

    params = {
        "symbols": symbol,
        "timeframe": "5Min",
        "start": start_time.isoformat().replace("+00:00", "Z"),
        "end": end_time.isoformat().replace("+00:00", "Z"),
        "limit": 10000,
        "feed": "iex"
    }

    response = requests.get(url, headers=get_headers(), params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(data)

    if "bars" not in data or symbol not in data["bars"]:
        raise Exception(f"no historical data found for {symbol}")

    df = pd.DataFrame(data["bars"][symbol])
    df["t"] = pd.to_datetime(df["t"])

    return df


def make_candlestick_chart(df, symbol):
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

    fig, axes = mpf.plot(
        plot_df,
        type="candle",
        volume=True,
        title=f"{symbol.upper()} 5-minute chart",
        ylabel="price",
        ylabel_lower="volume",
        returnfig=True
    )

    return fig