# tests/test_backtest.py
import pandas as pd
from src.backtest import backtest

def test_backtest():
    data = {
        "close": [100, 98, 95, 105],
        "signal": [0, 1, -1, 0],  # buy at second bar, sell at third
    }
    df = pd.DataFrame(data)
    final_balance = backtest(df, initial_capital=1000)
    # If we buy at 98 and sell at 95, we lose some capital
    assert final_balance < 1000, "Expected a loss!"
