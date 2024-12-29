# file: src/strategies/catch_the_wave.py
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator


def catch_the_wave_signals(
    df: pd.DataFrame,
    ma_period: int = 50,
    rsi_period: int = 14,
    rsi_oversold: float = 30,
    rsi_overbought: float = 70,
    rsi_threshold: float = None,
    use_ma_slope: bool = False,
    slope_threshold: float = 0.001,  # New threshold parameter
) -> pd.DataFrame:
    # Ensure necessary columns are present
    required_columns = ["open", "close", "high", "low"]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Moving Average
    sma = SMAIndicator(close=df["close"], window=ma_period)
    df["ma"] = sma.sma_indicator()

    # RSI
    rsi = RSIIndicator(close=df["close"], window=rsi_period)
    df["rsi"] = rsi.rsi()

    # Trend determination
    df["trend"] = df["close"] > df["ma"]
    if use_ma_slope:
        df["ma_slope"] = df["ma"].diff() / df["ma"]  # Normalized slope
        df["trend"] = df["trend"] & (df["ma_slope"] > slope_threshold)

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

    # Pullback zone
    df["pullback_zone"] = df["close"].between(df["ma"] * 0.98, df["ma"] * 1.02)

    # RSI condition
    df["rsi_condition"] = (df["rsi"] < rsi_overbought) & (
        df["rsi"] > (rsi_threshold if rsi_threshold else -float("inf"))
    )

    # Entry signal
    df["signal"] = (
        (df["trend"])
        & (df["pullback_zone"])
        & (df["is_hammer"] | df["is_engulfing"] | df["is_doji"])
        & (df["rsi_condition"])
    ).astype(int)

    # Exit signal
    df["exit_signal"] = (df["rsi"] > rsi_overbought).astype(int)

    return df


def catch_the_wave_exit(df: pd.DataFrame, rsi_overbought: float = 70) -> pd.DataFrame:
    # Check for required columns
    if "rsi" not in df.columns:
        raise ValueError("Input DataFrame must contain an 'rsi' column.")

    # Add exit signal based on RSI overbought
    df["exit_signal"] = 0
    exit_condition = df["rsi"] > rsi_overbought
    df.loc[exit_condition, "exit_signal"] = 1

    return df
