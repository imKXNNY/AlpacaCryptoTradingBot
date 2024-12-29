# tests/test_strategies/test_stuck_in_a_box.py

import pytest
import pandas as pd
import ast
from src.strategies.stuck_in_a_box import (
    stuck_in_a_box_signals,
    stuck_in_a_box_exit,
    identify_box  # Included if you plan to use it in tests
)


def test_stuck_in_a_box_signals_basic(solusdt_1h_data):
    """
    Test basic signal generation for the 'stuck_in_a_box' strategy.
    """
    df = solusdt_1h_data.copy()

    # Ensure necessary columns are present
    required_columns = {"open", "close", "high", "low"}
    assert required_columns.issubset(df.columns), (
        f"Missing columns: {required_columns - set(df.columns)}"
    )

    # Use smaller box_period and lower RSI thresholds to increase signal likelihood
    result = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Assert expected columns exist
    expected_columns = [
        'box_high', 'box_low', 'box_mid', 'rsi',
        'is_hammer', 'is_engulfing', 'is_doji',
        'near_support', 'entry_confirmation',
        'signal', 'exit_signal'
    ]
    assert all(col in result.columns for col in expected_columns), (
        "Some expected columns are missing."
    )

    # Assert no NaN values in key columns beyond the rolling window
    assert not result['signal'].iloc[5:].isna().any(), "NaN values found in 'signal' column."
    assert not result['exit_signal'].iloc[5:].isna().any(), "NaN values found in 'exit_signal' column."

    # Assert signals are binary (0 or 1)
    assert set(result['signal'].unique()).issubset({0, 1}), (
        "'signal' column contains non-binary values."
    )
    assert set(result['exit_signal'].unique()).issubset({0, 1}), (
        "'exit_signal' column contains non-binary values."
    )

    # Assert there are buy signals when conditions are met
    buy_signals = (result["signal"] == 1).sum()
    assert buy_signals > 0, f"Expected at least one buy signal; got {buy_signals}"


def test_stuck_in_a_box_signals_candlestick_patterns(solusdt_1h_data):
    """
    Test detection of specific candlestick patterns: hammer, engulfing, and doji.
    """
    df = solusdt_1h_data.copy()

    # Manipulate DataFrame to create specific candlestick patterns

    # Adding a hammer at index 10
    df.loc[10, 'open'] = 100
    df.loc[10, 'close'] = 110
    df.loc[10, 'high'] = 131  # Ensures (high - close) > 2*(close - open)
    df.loc[10, 'low'] = 95

    # Adding an engulfing pattern between index 19 (bearish) and 20 (bullish)
    if len(df) > 20:
        # Previous candle (index 19) - Bearish
        df.loc[19, 'open'] = 120
        df.loc[19, 'close'] = 115
        df.loc[19, 'high'] = 120
        df.loc[19, 'low'] = 114

        # Current candle (index 20) - Bullish and engulfing
        df.loc[20, 'open'] = 113  # Must be less than previous low (114)
        df.loc[20, 'close'] = 121  # Must be greater than previous high (120)
        df.loc[20, 'high'] = 121
        df.loc[20, 'low'] = 113

    # Adding a doji at index 30
    df.loc[30, 'open'] = 130
    df.loc[30, 'close'] = 130
    df.loc[30, 'high'] = 131
    df.loc[30, 'low'] = 129

    result = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Assert candlestick patterns are detected
    assert 'is_hammer' in result.columns, "'is_hammer' column missing."
    assert 'is_engulfing' in result.columns, "'is_engulfing' column missing."
    assert 'is_doji' in result.columns, "'is_doji' column missing."

    # Check specific rows for patterns
    assert result.at[10, 'is_hammer'] == 1, "Hammer pattern not detected correctly."

    if len(df) > 20:
        assert result.at[20, 'is_engulfing'] == 1, "Engulfing pattern not detected correctly."

    assert result.at[30, 'is_doji'] == 1, "Doji pattern not detected correctly."


def test_stuck_in_a_box_missing_columns():
    """
    Test that the strategy raises a ValueError when required columns are missing.
    """
    # Prepare DataFrame missing required columns
    solusdt_df = pd.DataFrame({
        'close': [1, 2, 3]
    })

    with pytest.raises(ValueError) as exc_info:
        stuck_in_a_box_signals(solusdt_df)

    # Extract the missing columns from the exception message
    message = exc_info.value.args[0]
    missing_cols_str = message.split(": ")[1]
    missing_cols = ast.literal_eval(missing_cols_str)

    assert missing_cols == {'open', 'high', 'low'}, (
        f"Expected missing columns {{'open', 'high', 'low'}}, got {missing_cols}"
    )


def test_stuck_in_a_box_exit(solusdt_1h_data):
    """
    Test exit signal generation based on RSI overbought and proximity to box_high.
    """
    df = solusdt_1h_data.copy()

    # FIRST, run the signals logic which populates box_high, box_low, box_mid, rsi, etc.
    df = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Ensure necessary columns are present
    required_columns = {"close", "high", "low", "box_high", "box_low", "box_mid", "rsi"}
    assert required_columns.issubset(df.columns), (
        f"Missing columns: {required_columns - set(df.columns)}"
    )

    # Run exit logic
    result = stuck_in_a_box_exit(
        df,
        rsi_overbought=70,
        near_threshold=0.02
    )

    assert "exit_signal" in result.columns, "'exit_signal' column not found in result."

    # We expect exit signals where close is near box_high or RSI > 70
    exit_signals = (result["exit_signal"] == 1).sum()
    assert exit_signals >= 0, f"Expected exit signals; got {exit_signals}"

    # Optionally, check specific conditions
    expected_exit = (result["close"] >= result["box_high"] * (1 - 0.02)) | (result["rsi"] > 70)
    actual_exit = result["exit_signal"] == 1
    assert actual_exit.equals(expected_exit.fillna(False)), (
        "Exit signals do not match expected conditions."
    )


def test_stuck_in_a_box_validate_range(solusdt_1h_data):
    """
    Placeholder for future validation logic on box formation.
    Currently, no 'validate_range' is implemented.
    """
    df = solusdt_1h_data.copy()

    # Since 'validate_range' is not implemented, this test ensures that the function runs without errors
    result = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Add assertions as needed
    assert not result.empty, "Resulting DataFrame is empty."
    assert 'signal' in result.columns, "'signal' column not found in result."

    buy_signals = (result["signal"] == 1).sum()
    assert buy_signals >= 0, "No error should occur even if no signals."


def test_stuck_in_a_box_small_dataframe():
    """
    Test the strategy's behavior with a small dataset.
    """
    # Create a small DataFrame with only a few rows
    small_df = pd.DataFrame({
        'open': [100, 105],
        'close': [105, 102],
        'high': [106, 107],
        'low': [99, 101]
    })

    result = stuck_in_a_box_signals(
        small_df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Assert no errors occur
    assert not result.empty, "Resulting DataFrame is empty for a small dataset."
    assert 'signal' in result.columns, "'signal' column missing."
    assert 'exit_signal' in result.columns, "'exit_signal' column missing."

    # Signals should be binary
    assert set(result['signal'].unique()).issubset({0, 1}), (
        "'signal' column contains non-binary values."
    )
    assert set(result['exit_signal'].unique()).issubset({0, 1}), (
        "'exit_signal' column contains non-binary values."
    )

    # Ensure that even with small data, calculations are performed
    assert 'box_high' in result.columns, "'box_high' column missing."
    assert 'box_low' in result.columns, "'box_low' column missing."
    assert 'box_mid' in result.columns, "'box_mid' column missing."
    assert 'rsi' in result.columns, "'rsi' column missing."


@pytest.mark.parametrize(
    "box_period, rsi_period, rsi_threshold, rsi_oversold, near_threshold, expected_min_signals",
    [
        (5, 3, 50, 60, 0.02, 1),  # Basic configuration
        (10, 5, 55, 65, 0.03, 2),  # Different parameters
        (20, 10, 60, 70, 0.05, 0),  # Larger box_period, expecting no signals
    ]
)
def test_stuck_in_a_box_parameterized(
    solusdt_1h_data,
    box_period, rsi_period, rsi_threshold, rsi_oversold,
    near_threshold, expected_min_signals
):
    """
    Parameterized tests to cover various configurations of the 'stuck_in_a_box' strategy.
    """
    df = solusdt_1h_data.copy()

    result = stuck_in_a_box_signals(
        df,
        box_period=box_period,
        rsi_period=rsi_period,
        rsi_threshold=rsi_threshold,
        rsi_oversold=rsi_oversold,
        near_threshold=near_threshold
    )

    # Assert expected columns exist
    expected_columns = [
        'box_high', 'box_low', 'box_mid', 'rsi',
        'is_hammer', 'is_engulfing', 'is_doji',
        'near_support', 'entry_confirmation',
        'signal', 'exit_signal'
    ]
    assert all(col in result.columns for col in expected_columns), (
        "Some expected columns are missing."
    )

    # Assert signals are binary
    assert set(result['signal'].unique()).issubset({0, 1}), (
        "'signal' column contains non-binary values."
    )
    assert set(result['exit_signal'].unique()).issubset({0, 1}), (
        "'exit_signal' column contains non-binary values."
    )

    # Check if signals meet expectations
    buy_signals = (result["signal"] == 1).sum()
    assert buy_signals >= expected_min_signals, (
        f"Expected at least {expected_min_signals} buy signals; got {buy_signals}"
    )


def test_identify_box(solusdt_1h_data):
    """
    Test the 'identify_box' function to ensure it correctly identifies box ranges.
    """
    df = solusdt_1h_data.copy()

    # Use a specific box_period
    box_period = 2
    result = identify_box(df, period=box_period)

    # Assert expected columns exist
    expected_columns = ['box_high', 'box_bottom']
    assert all(col in result.columns for col in expected_columns), (
        "Some expected columns are missing in 'identify_box'."
    )

    # Check rolling calculations
    expected_box_high = df['high'].rolling(window=box_period).max()
    expected_box_bottom = df['low'].rolling(window=box_period).min()
    pd.testing.assert_series_equal(
        result['box_high'],
        expected_box_high,
        check_names=False,
        check_dtype=False
    )
    pd.testing.assert_series_equal(
        result['box_bottom'],
        expected_box_bottom,
        check_names=False,
        check_dtype=False
    )


def test_stuck_in_a_box_no_signals(solusdt_1h_data):
    """
    Test the strategy when no signals should be generated.
    """
    df = solusdt_1h_data.copy()

    # FIRST, run the signals logic which populates box_high, box_low, box_mid, rsi, etc.
    df = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Manipulate DataFrame to ensure no signals
    # Set 'close' far above 'box_high' and 'rsi' above oversold threshold
    df['close'] = df['box_high'] * 1.1  # Now 'box_high' exists
    df['rsi'] = 80  # Above oversold threshold

    # Re-run signal generation after manipulation
    df = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Assert no buy signals
    buy_signals = (df["signal"] == 1).sum()
    assert buy_signals == 0, f"Expected no buy signals; got {buy_signals}"


def test_stuck_in_a_box_full_flow(solusdt_1h_data):
    """
    Test the full flow: signal generation followed by exit signal generation.
    """
    df = solusdt_1h_data.copy()

    # Run signal generation
    df = stuck_in_a_box_signals(
        df,
        box_period=5,
        rsi_period=3,
        rsi_threshold=50,
        rsi_oversold=60,
        near_threshold=0.02
    )

    # Run exit signal generation
    df = stuck_in_a_box_exit(
        df,
        rsi_overbought=70,
        near_threshold=0.02
    )

    # Assert that 'exit_signal' exists
    assert "exit_signal" in df.columns, "'exit_signal' column not found in result."

    # Optionally, check that exit signals are correctly set
    expected_exit = (df["close"] >= df["box_high"] * (1 - 0.02)) | (df["rsi"] > 70)
    actual_exit = df["exit_signal"] == 1
    assert actual_exit.equals(expected_exit.fillna(False)), (
        "Exit signals do not match expected conditions."
    )
