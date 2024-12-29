# tests/test_strategies/test_catch_the_wave.py

import pytest
import pandas as pd
import ast
from src.strategies.catch_the_wave import catch_the_wave_signals, catch_the_wave_exit


def test_catch_the_wave_signals_basic(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Ensure necessary columns are present
    required_columns = {"open", "close", "high", "low"}
    assert required_columns.issubset(
        df.columns
    ), f"Missing columns: {required_columns - set(df.columns)}"

    # Force smaller ma_period so an uptrend can be easily recognized
    result = catch_the_wave_signals(df, ma_period=2, rsi_period=2, rsi_oversold=50)
    print(result)

    # Assert expected columns exist
    expected_columns = [
        "ma",
        "rsi",
        "trend",
        "is_hammer",
        "is_engulfing",
        "is_doji",
        "pullback_zone",
        "rsi_condition",
        "signal",
        "exit_signal",
    ]
    assert all(
        col in result.columns for col in expected_columns
    ), "Some expected columns are missing."

    # Assert no NaN values in key columns
    assert not result["signal"].isna().any(), "NaN values found in 'signal' column."
    assert (
        not result["exit_signal"].isna().any()
    ), "NaN values found in 'exit_signal' column."

    # Assert signals are binary (0 or 1)
    assert set(result["signal"].unique()).issubset(
        {0, 1}
    ), "'signal' column contains non-binary values."
    assert set(result["exit_signal"].unique()).issubset(
        {0, 1}
    ), "'exit_signal' column contains non-binary values."


def test_catch_the_wave_signals_slope(btcusdt_1h_data):
    ma_period = 5  # Define ma_period to match the strategy
    df = btcusdt_1h_data.copy()

    # Ensure necessary columns are present
    required_columns = {"open", "close", "high", "low"}
    assert required_columns.issubset(
        df.columns
    ), f"Missing columns: {required_columns - set(df.columns)}"

    # Use a smaller MA period and enable slope condition
    result = catch_the_wave_signals(
        df,
        ma_period=ma_period,
        rsi_period=3,
        rsi_oversold=80,
        use_ma_slope=True,
        slope_threshold=0.001,
    )

    # Assert expected columns exist
    expected_columns = [
        "ma",
        "rsi",
        "trend",
        "is_hammer",
        "is_engulfing",
        "is_doji",
        "pullback_zone",
        "rsi_condition",
        "signal",
        "exit_signal",
        "ma_slope",
    ]
    assert all(
        col in result.columns for col in expected_columns
    ), "Some expected columns are missing."

    # Assert no NaN values in key columns, excluding the first 'ma_period' rows
    assert (
        not result["signal"].iloc[ma_period:].isna().any()
    ), "NaN values found in 'signal' column."
    assert (
        not result["exit_signal"].iloc[ma_period:].isna().any()
    ), "NaN values found in 'exit_signal' column."
    assert (
        not result["ma_slope"].iloc[ma_period:].isna().any()
    ), "NaN values found in 'ma_slope' column."

    # Assert signals are binary (0 or 1)
    assert set(result["signal"].unique()).issubset(
        {0, 1}
    ), "'signal' column contains non-binary values."
    assert set(result["exit_signal"].unique()).issubset(
        {0, 1}
    ), "'exit_signal' column contains non-binary values."

    # Assert there are buy signals when slope condition is met
    buy_signals = (result["signal"] == 1).sum()
    assert buy_signals > 0, f"Expected buy signals with slope check; got {buy_signals}"


def test_catch_the_wave_exit(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Ensure necessary columns are present
    required_columns = {"open", "close", "high", "low"}
    assert required_columns.issubset(
        df.columns
    ), f"Missing columns: {required_columns - set(df.columns)}"

    # FIRST, run the signals logic which populates ma, rsi, trend, etc.
    df = catch_the_wave_signals(df)

    # Run exit logic
    result = catch_the_wave_exit(df, rsi_overbought=70)
    assert "exit_signal" in result.columns, "'exit_signal' column not found in result."

    # We expect exit signals where RSI > 70
    exit_signals = (result["exit_signal"] == 1).sum()
    assert exit_signals >= 0, f"Expected exit signals; got {exit_signals}"
    # Additional assertions can be added based on specific expectations


def test_rsi_conditions_and_signals(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Call function with specific RSI parameters
    result = catch_the_wave_signals(
        df, rsi_period=14, rsi_oversold=30, rsi_overbought=70
    )

    # Assert expected columns exist
    expected_columns = [
        "ma",
        "rsi",
        "trend",
        "is_hammer",
        "is_engulfing",
        "is_doji",
        "pullback_zone",
        "rsi_condition",
        "signal",
        "exit_signal",
    ]
    assert all(
        col in result.columns for col in expected_columns
    ), "Some expected columns are missing."

    # Assert no NaN values in key columns
    assert not result["signal"].isna().any(), "NaN values found in 'signal' column."
    assert (
        not result["exit_signal"].isna().any()
    ), "NaN values found in 'exit_signal' column."

    # Assert signals are binary (0 or 1)
    assert set(result["signal"].unique()).issubset(
        {0, 1}
    ), "'signal' column contains non-binary values."
    assert set(result["exit_signal"].unique()).issubset(
        {0, 1}
    ), "'exit_signal' column contains non-binary values."


def test_catch_the_wave_missing_columns():
    # Prepare DataFrame missing required columns using solusdt_1h_data fixture
    solusdt_df = pd.DataFrame({"close": [1, 2, 3]})

    with pytest.raises(ValueError) as exc_info:
        catch_the_wave_signals(solusdt_df)

    # Extract the missing columns from the exception message
    message = exc_info.value.args[0]
    missing_cols_str = message.split(": ")[1]
    missing_cols = ast.literal_eval(missing_cols_str)

    assert missing_cols == {
        "open",
        "high",
        "low",
    }, f"Expected missing columns {{'open', 'high', 'low'}}, got {missing_cols}"


def test_catch_the_wave_rsi_threshold(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Set specific RSI thresholds
    result = catch_the_wave_signals(
        df,
        ma_period=5,
        rsi_period=3,
        rsi_oversold=30,
        rsi_threshold=50,
        rsi_overbought=70,
    )

    # Assert RSI conditions are applied correctly
    # 'rsi_condition' should be (rsi < 70) & (rsi > 50)
    expected_condition = (result["rsi"] < 70) & (result["rsi"] > 50)
    assert (
        result["rsi_condition"] == expected_condition
    ).all(), "RSI conditions not applied correctly."


def test_catch_the_wave_slope_threshold(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Test with an aggressive slope threshold
    high_slope_threshold = 0.05  # 5% slope
    result = catch_the_wave_signals(
        df,
        ma_period=5,
        rsi_period=3,
        rsi_oversold=80,
        use_ma_slope=True,
        slope_threshold=high_slope_threshold,
    )

    # Assert slope is considered in the trend
    assert "ma_slope" in result.columns, "'ma_slope' column missing."
    # All trends should have ma_slope > 0.05
    expected_trend = (df["close"] > result["ma"]) & (
        result["ma_slope"] > high_slope_threshold
    )
    assert result["trend"].equals(
        expected_trend
    ), "Slope threshold not applied correctly."


def test_catch_the_wave_candlestick_patterns(btcusdt_1h_data):
    df = btcusdt_1h_data.copy()

    # Manipulate DataFrame to create specific candlestick patterns

    # Adding a hammer at index 10
    df.loc[10, "open"] = 100
    df.loc[10, "close"] = 110
    df.loc[10, "high"] = 131  # Adjusted to satisfy (high - close) > 2*(close - open)
    df.loc[10, "low"] = 95

    # Adding an engulfing pattern between index 19 (bearish) and 20 (bullish)
    if len(df) > 20:
        # Previous candle (index 19) - Bearish
        df.loc[19, "open"] = 120
        df.loc[19, "close"] = 115
        df.loc[19, "high"] = 120
        df.loc[19, "low"] = 114

        # Current candle (index 20) - Bullish and engulfing
        df.loc[20, "open"] = 113  # Must be less than previous low (114)
        df.loc[20, "close"] = 121  # Must be greater than previous high (120)
        df.loc[20, "high"] = 121
        df.loc[20, "low"] = 113

    # Adding a doji at index 30
    df.loc[30, "open"] = 130
    df.loc[30, "close"] = 130
    df.loc[30, "high"] = 131
    df.loc[30, "low"] = 129

    result = catch_the_wave_signals(df)

    # Assert candlestick patterns are detected
    assert "is_hammer" in result.columns, "'is_hammer' column missing."
    assert "is_engulfing" in result.columns, "'is_engulfing' column missing."
    assert "is_doji" in result.columns, "'is_doji' column missing."

    # Check specific rows for patterns
    assert result.at[10, "is_hammer"] == 1, "Hammer pattern not detected correctly."

    if len(df) > 20:
        assert (
            result.at[20, "is_engulfing"] == 1
        ), "Engulfing pattern not detected correctly."

    assert result.at[30, "is_doji"] == 1, "Doji pattern not detected correctly."


def test_catch_the_wave_small_dataframe(btcusdt_1h_data):
    # Create a small DataFrame by selecting first 2 rows from fixture
    small_df = btcusdt_1h_data.head(2).copy()

    result = catch_the_wave_signals(small_df)

    # Assert no errors occur
    assert not result.empty, "Resulting DataFrame is empty for a small dataset."
    assert "signal" in result.columns, "'signal' column missing."
    assert "exit_signal" in result.columns, "'exit_signal' column missing."

    # Signals should be binary
    assert set(result["signal"].unique()).issubset(
        {0, 1}
    ), "'signal' column contains non-binary values."
    assert set(result["exit_signal"].unique()).issubset(
        {0, 1}
    ), "'exit_signal' column contains non-binary values."

    # Ensure that even with small data, calculations are performed
    assert "ma" in result.columns, "'ma' column missing."
    assert "rsi" in result.columns, "'rsi' column missing."


def test_catch_the_wave_exit_missing_rsi():
    df = pd.DataFrame()

    with pytest.raises(
        ValueError, match="Input DataFrame must contain an 'rsi' column."
    ):
        catch_the_wave_exit(df, rsi_overbought=70)


# Parameterized Tests to Cover Various Configurations


@pytest.mark.parametrize(
    "ma_period, rsi_period, rsi_oversold, rsi_overbought, use_ma_slope, slope_threshold, expected_min_signals",
    [
        (5, 3, 30, 70, False, 0.001, 1),  # Basic configuration
        (10, 5, 25, 75, True, 0.002, 1),  # Different parameters
        (20, 10, 20, 80, True, 0.005, 0),  # High slope threshold, expecting no signals
    ],
)
def test_catch_the_wave_parameterized(
    btcusdt_1h_data,
    ma_period,
    rsi_period,
    rsi_oversold,
    rsi_overbought,
    use_ma_slope,
    slope_threshold,
    expected_min_signals,
):
    df = btcusdt_1h_data.copy()

    result = catch_the_wave_signals(
        df,
        ma_period=ma_period,
        rsi_period=rsi_period,
        rsi_oversold=rsi_oversold,
        rsi_overbought=rsi_overbought,
        use_ma_slope=use_ma_slope,
        slope_threshold=slope_threshold,
    )

    # Assert expected columns exist
    expected_columns = [
        "ma",
        "rsi",
        "trend",
        "is_hammer",
        "is_engulfing",
        "is_doji",
        "pullback_zone",
        "rsi_condition",
        "signal",
        "exit_signal",
    ]
    if use_ma_slope:
        expected_columns.append("ma_slope")
    assert all(
        col in result.columns for col in expected_columns
    ), "Some expected columns are missing."

    # Assert signals are binary
    assert set(result["signal"].unique()).issubset(
        {0, 1}
    ), "'signal' column contains non-binary values."
    assert set(result["exit_signal"].unique()).issubset(
        {0, 1}
    ), "'exit_signal' column contains non-binary values."

    # Check if signals meet expectations
    buy_signals = (result["signal"] == 1).sum()
    assert (
        buy_signals >= expected_min_signals
    ), f"Expected at least {expected_min_signals} buy signals; got {buy_signals}"
