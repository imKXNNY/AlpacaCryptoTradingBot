# file: src/strategies/stuck_in_a_box.py
import pandas as pd
from ta.momentum import RSIIndicator


def identify_box(df: pd.DataFrame, period: int = 50) -> pd.DataFrame:
    """
    Identify a 'box' range over the last `period` bars.
    """
    df["box_high"] = df["high"].rolling(period).max()
    df["box_bottom"] = df["low"].rolling(period).min()

    # TODO: Consider adding validation for box formation
    # Examples:
    # - Ensure the range is tight enough (e.g., width < 10% of box_bottom).
    # - This could help avoid false signals in trending markets.
    return df


def stuck_in_a_box_signals(
    df: pd.DataFrame,
    box_period: int = 50,
    rsi_period: int = 14,
    rsi_threshold: float = 50,
    rsi_oversold: float = 30,
    near_threshold: float = 0.02,
) -> pd.DataFrame:
    # Ensure necessary columns are present
    required_columns = ["open", "close", "high", "low"]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Box calculation
    df["box_high"] = df["high"].rolling(window=box_period).max()
    df["box_low"] = df["low"].rolling(window=box_period).min()
    df["box_mid"] = (df["box_high"] + df["box_low"]) / 2

    # RSI
    rsi = RSIIndicator(close=df["close"], window=rsi_period)
    df["rsi"] = rsi.rsi()

    # Candlestick patterns
    df["is_hammer"] = (
        (df["close"] > df["open"])
        & (df["low"] == df["low"].rolling(window=5).min())
        & ((df["high"] - df["close"]) > 2 * (df["close"] - df["open"]))
    )
    df["is_engulfing"] = (
        (df["close"].shift(1) < df["open"].shift(1))
        & (df["close"] > df["open"])
        & (df["close"] > df["high"].shift(1))
        & (df["open"] < df["low"].shift(1))
    )
    df["is_doji"] = abs(df["close"] - df["open"]) < (df["high"] - df["low"]) * 0.1

    # Entry condition
    df["near_support"] = df["close"].between(
        df["box_low"] * (1 - near_threshold), df["box_low"] * (1 + near_threshold)
    )
    df["entry_confirmation"] = df["rsi"] > rsi_threshold

    df["signal"] = (
        (df["near_support"])
        & (df["is_hammer"] | df["is_engulfing"] | df["is_doji"])
        & (df["entry_confirmation"])
        & (df["rsi"] < rsi_oversold)
    ).astype(int)

    # Exit condition
    df["near_top"] = df["close"] >= df["box_high"] * (1 - near_threshold)
    df["exit_signal"] = (df["near_top"] | (df["rsi"] > rsi_oversold)).astype(int)

    return df


def stuck_in_a_box_exit(
    df: pd.DataFrame, rsi_overbought: float = 70, near_threshold: float = 0.02
) -> pd.DataFrame:
    """
    Example exit near 'box_high' or RSI overbought.
    'exit_signal' = 1 means 'exit/sell'
    """
    df["exit_signal"] = 0
    near_top = df["close"] >= df["box_high"] * (1 - near_threshold)
    overbought = df["rsi"] > rsi_overbought

    df.loc[near_top | overbought, "exit_signal"] = 1

    # TODO: Add stop-loss logic for exits
    # Example:
    # - Use an ATR-based stop-loss set below the box bottom for long positions.

    return df
