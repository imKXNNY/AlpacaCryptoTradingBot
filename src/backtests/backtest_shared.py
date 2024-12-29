# src/backtests/backtest_shared.py
import os
import pandas as pd
import backtrader as bt


class LowercasePandasData(bt.feeds.PandasData):
    """
    Custom feed for columns: 'timestamp', 'open','high','low','close','volume'.
    """

    params = (
        ("datetime", "timestamp"),  # Column name for datetime
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", None),
    )


def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads CSV columns => 'timestamp','open','high','low','close','volume'
    Ensures 'timestamp' is parsed as datetime.
    """
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def run_backtest(
    bt_strategy,
    data_filepath: str,
    initial_cash: float = 10000.0,
    commission: float = 0.001,
) -> float:
    df = load_data(data_filepath)
    print(df.head())  # Debug: Ensure data is loaded correctly

    data_feed = LowercasePandasData(dataname=df)

    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.addstrategy(bt_strategy)
    cerebro.broker.setcash(initial_cash)

    # Set commission - 0.1% per trade
    cerebro.broker.setcommission(commission=commission)

    # Add Slippage
    cerebro.broker.set_slippage_perc(perc=0.001)  # 0.1% slippage

    _ = cerebro.run()  # Run & Discard
    final_value = cerebro.broker.getvalue()
    print(f"Final portfolio value: {final_value:.2f}")
    return final_value


def preprocess_binance_csv(input_filepath: str, output_filepath: str):
    """
    Standardizes Binance CSV files for backtesting.
    - Adds headers: 'timestamp', 'open', 'high', 'low', 'close', 'volume'.
    - Converts 'timestamp' from Unix to UTC datetime.
    - Saves cleaned data to the specified output path.
    """
    # Load the CSV without headers
    df = pd.read_csv(input_filepath, header=None)

    # Assign Binance column names
    df.columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore",
    ]

    # Convert 'timestamp' from Unix to UTC datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    # Retain only relevant columns
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    # Save the cleaned file
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    df.to_csv(output_filepath, index=False)
    print(f"Processed file saved to: {output_filepath}")
