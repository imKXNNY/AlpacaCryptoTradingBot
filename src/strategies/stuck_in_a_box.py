# file: src/strategies/stuck_in_a_box.py
import pandas as pd
import pandas_ta as ta

def identify_box(df: pd.DataFrame, period: int = 50) -> pd.DataFrame:
    """
    Rough example to identify a 'box' range over the last `period`.
    We find recent max (resistance) and min (support).
    """
    df["box_top"] = df["High"].rolling(period).max()
    df["box_bottom"] = df["Low"].rolling(period).min()
    return df

def stuck_in_a_box_signals(
    df: pd.DataFrame,
    rsi_period: int = 14,
    rsi_oversold: float = 30,
    box_period: int = 50
) -> pd.DataFrame:
    """
    Generate signals for range trading:
    - Go long near box_bottom when RSI is oversold.
    - Example: Exits near box_top or when RSI is overbought.

    Returns a DataFrame with 'signal' column for entries.
    """
    # 1. Identify the 'box' over a rolling period
    df = identify_box(df, period=box_period)

    # 2. Calculate RSI
    df["rsi"] = ta.rsi(df["Close"], length=rsi_period)

    # 3. Entry condition: Price near box_bottom + RSI oversold
    df["signal"] = 0
    # For "near box_bottom", define a threshold or percent
    near_bottom = (df["Close"] <= df["box_bottom"] * 1.02)  # e.g. 2% above bottom
    oversold = (df["rsi"] < rsi_oversold)

    df.loc[near_bottom & oversold, "signal"] = 1  # buy

    return df

def stuck_in_a_box_exit(
    df: pd.DataFrame,
    rsi_overbought: float = 70
) -> pd.DataFrame:
    """
    Example exit near 'box_top' or when RSI is overbought.
    """
    df["exit_signal"] = 0
    near_top = (df["Close"] >= df["box_top"] * 0.98)  # within 2% of top
    overbought = (df["rsi"] > rsi_overbought)

    # You can combine conditions or treat them separately
    df.loc[near_top | overbought, "exit_signal"] = 1
    return df
