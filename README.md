# mini market data terminal

a simple streamlit app that shows:

* a historical 5-minute candlestick chart for a stock
* live bid / ask / trade updates using alpaca streaming data

## setup

install the required packages:

```bash
pip install -r requirements.txt
```

create a `.env` file in the project folder:

```env
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

## run the app

```bash
streamlit run app.py
```

## files

```txt
app.py
data_connector.py
stream_quotes.py
requirements.txt
README.md
.env
```

## what each file does

`app.py`
runs the streamlit interface.

`data_connector.py`
gets historical stock bars from alpaca and builds the candlestick chart.

`stream_quotes.py`
streams live stock quotes and trades.

`requirements.txt`
lists the python packages needed to run the app.

`.env`
stores alpaca api keys. this file should not be uploaded publicly.

## notes

this app currently supports stocks only, not crypto.

historical data uses alpaca's iex feed.

live market data comes from the streaming file.
