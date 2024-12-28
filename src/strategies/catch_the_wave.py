# file: src/strategies/catch_the_wave.py
import pandas as pd
import pandas_ta as ta

def catch_the_wave_signals(
    df: pd.DataFrame,
    ma_period: int = 50,
    rsi_period: int = 14,
    rsi_oversold: float = 30
) -> pd.DataFrame:
    """
    Generate 'Catch the Wave' trade signals in a trending market:
    - Uptrend if close is above 50-MA (or 50-MA slope is positive).
    - RSI oversold for entry.
    - Optional: Candle pattern check.

    Returns a DataFrame with new columns 'trend', 'signal'.
    'signal' = 1 means 'buy/long entry', 0 means 'no signal'
    """

    # 1. Calculate 50-MA, RSI
    df["ma50"] = df["Close"].rolling(ma_period).mean()
    df["rsi"] = ta.rsi(df["Close"], length=rsi_period)

    # Mark uptrend (simple check: close above MA)
    df["trend"] = (df["Close"] > df["ma50"]).astype(int)

    # More robust check: slope of MA
    # df["ma50_slope"] = df["ma50"].diff()
    # df["trend"] = (df["ma50_slope"] > 0).astype(int)

    # 2. Identify pullback (RSI oversold) in uptrend
    df["signal"] = 0
    buy_condition = (df["trend"] == 1) & (df["rsi"] < rsi_oversold)
    df.loc[buy_condition, "signal"] = 1

    return df

def catch_the_wave_exit(
    df: pd.DataFrame,
    rsi_overbought: float = 70
) -> pd.DataFrame:
    """
    Optional exit logic: Exit near previous swing high or RSI overbought.
    'exit_signal' = 1 means 'exit/sell'
    """
    df["exit_signal"] = 0
    exit_condition = (df["rsi"] > rsi_overbought)
    df.loc[exit_condition, "exit_signal"] = 1
    return df
