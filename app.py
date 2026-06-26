import os
import time
import threading
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from alpaca.data.live.stock import StockDataStream
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.enums import DataFeed

from data_connector import get_historical_bars, make_candlestick_chart

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

latest_data = {
    "symbol": "none",
    "bid": "waiting...",
    "ask": "waiting...",
    "last_trade": "waiting...",
    "quote_time": "waiting...",
    "trade_time": "waiting..."
}


def is_crypto_symbol(symbol):
    return "/" in symbol


def run_stock_stream(symbol):
    stream = StockDataStream(
        API_KEY,
        SECRET_KEY,
        feed=DataFeed.IEX
    )

    async def quote_handler(quote):
        latest_data["symbol"] = quote.symbol
        latest_data["bid"] = quote.bid_price
        latest_data["ask"] = quote.ask_price
        latest_data["quote_time"] = quote.timestamp

    async def trade_handler(trade):
        latest_data["symbol"] = trade.symbol
        latest_data["last_trade"] = trade.price
        latest_data["trade_time"] = trade.timestamp

    stream.subscribe_quotes(quote_handler, symbol)
    stream.subscribe_trades(trade_handler, symbol)

    stream.run()

def run_crypto_stream(symbol):
    stream = CryptoDataStream(API_KEY, SECRET_KEY)

    async def quote_handler(quote):
        latest_data["symbol"] = quote.symbol
        latest_data["bid"] = quote.bid_price
        latest_data["ask"] = quote.ask_price
        latest_data["quote_time"] = quote.timestamp

    async def trade_handler(trade):
        latest_data["symbol"] = trade.symbol
        latest_data["last_trade"] = trade.price
        latest_data["trade_time"] = trade.timestamp

    stream.subscribe_quotes(quote_handler, symbol)
    stream.subscribe_trades(trade_handler, symbol)

    stream.run()


def start_stream(symbol):
    if is_crypto_symbol(symbol):
        thread = threading.Thread(
            target=run_crypto_stream,
            args=(symbol,),
            daemon=True
        )
    else:
        thread = threading.Thread(
            target=run_stock_stream,
            args=(symbol,),
            daemon=True
        )

    thread.start()


st.set_page_config(
    page_title="market data terminal",
    layout="wide"
)

st.title("market data terminal")

st.divider()

st.header("1. historical ohlcv chart")

historical_symbol = st.text_input(
    "enter stock ticker for historical chart",
    "AAPL"
).upper().strip()

if st.button("load historical chart"):
    try:
        with st.spinner(f"loading historical ohlcv data for {historical_symbol}..."):
            df = get_historical_bars(historical_symbol)
            fig = make_candlestick_chart(df, historical_symbol)

        st.pyplot(fig)
        plt.close(fig)

        st.subheader("recent raw ohlcv data")
        st.dataframe(df.reset_index(drop=True))

    except Exception as e:
        st.error(f"could not load historical data for {historical_symbol}.")
        st.write(e)

st.divider()

st.header("2. real-time websocket quote stream")

live_symbol = st.text_input(
    "enter any stock ticker or crypto symbol",
    "AAPL"
).upper().strip()

st.caption("examples: aapl, tsla, spy, nvda, btc/usd, eth/usd")

if st.button("start websocket stream"):
    start_stream(live_symbol)

    st.info(f"streaming {live_symbol}.")

    symbol_box = st.empty()
    col1, col2, col3 = st.columns(3)
    bid_box = col1.empty()
    ask_box = col2.empty()
    trade_box = col3.empty()
    quote_time_box = st.empty()
    trade_time_box = st.empty()

    while True:
        symbol_box.write(f"symbol: {latest_data['symbol']}")

        bid_box.metric("current bid", latest_data["bid"])
        ask_box.metric("current ask", latest_data["ask"])
        trade_box.metric("last trade price", latest_data["last_trade"])

        quote_time_box.write(f"quote time: {latest_data['quote_time']}")
        trade_time_box.write(f"trade time: {latest_data['trade_time']}")

        time.sleep(1)
else:
    st.info("click 'start websocket stream' to begin live bid, ask, and last trade updates.")