# tests/test_backtest.py

from src.backtests.backtest_shared import preprocess_binance_csv, run_backtest
from src.backtests.backtest_catch_the_wave import backtest_catch_the_wave
from src.backtests.backtest_stuck_in_a_box import backtest_stuck_in_a_box  # Ensure this import exists

def test_backtest_catch_the_wave_with_binance_data():
    # Preprocess Binance CSV
    preprocess_binance_csv("data/BTCUSDT-1h-2024-11.csv", "tests/tmp-data/temp_cleaned_btcusdt_1h.csv")

    # Run backtest using the preprocessed data
    final_balance = backtest_catch_the_wave("tests/tmp-data/temp_cleaned_btcusdt_1h.csv", initial_cash=1000)
    assert final_balance != 1000.0, "Final balance should differ from initial cash."

def test_backtest_stuck_in_a_box_with_binance_data():
    # Preprocess Binance CSV for SOL/USDT
    preprocess_binance_csv("data/SOLUSDT-1h-2024-11.csv", "tests/tmp-data/temp_cleaned_solusdt_1h.csv")

    # Run backtest using the preprocessed data
    final_balance = backtest_stuck_in_a_box("tests/tmp-data/temp_cleaned_solusdt_1h.csv", initial_cash=1000)
    assert final_balance != 1000.0, "Final balance should differ from initial cash."
