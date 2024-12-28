# file: src/utils/data_fetch.py
import pandas as pd
import alpaca_trade_api as tradeapi
import logging
import os

API_KEY = os.getenv("ALPACA_API_KEY", "YOUR_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "YOUR_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version="v2")

def fetch_ohlcv(symbol: str, timeframe="1Hour", limit=500) -> pd.DataFrame:
    """
    Fetch historical OHLCV data from Alpaca, return as a Pandas DataFrame.
    """
    logging.info(f"Fetching {limit} bars for {symbol} on {timeframe}")
    bars = api.get_bars(symbol, timeframe, limit=limit).df
    # Adjust if needed (e.g., rename columns, ensure datetime index)
    bars.index = pd.to_datetime(bars.index)
    bars = bars.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    })
    return bars
