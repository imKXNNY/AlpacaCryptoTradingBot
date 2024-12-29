# File: src/backtests/backtest_stuck_in_a_box.py
# Description: Implement a simple backtest using the StuckInABox strategy.

import backtrader as bt
from backtests.backtest_shared import run_backtest

class StuckInABoxStrategy(bt.Strategy):
    """
    A Backtrader Strategy for 'Stuck in a Box':
    1) Identify box_top, box_bottom over 'box_period'
    2) If price near box_bottom AND RSI < rsi_oversold => buy
    3) If price near box_top OR RSI > rsi_overbought => sell

    TODO:
    - Validate the range is truly a 'box' (maybe width < 10%).
    - Integrate ATR-based stop-loss below box_bottom.
    - Candlestick confirmation near support.
    """

    params = {
        "box_period": 50,
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "near_threshold": 0.02,  # 2%
    }

    def __init__(self):
        # Rolling max/min
        self.box_top = bt.indicators.Highest(self.data.high, period=self.params.box_period)
        self.box_bottom = bt.indicators.Lowest(self.data.low, period=self.params.box_period)

        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.in_position = False

    def next(self):
        near_bottom = self.data.close[0] <= self.box_bottom[0] * (1 + self.params.near_threshold)
        oversold = self.rsi[0] < self.params.rsi_oversold

        # Buy condition
        if not self.in_position and near_bottom and oversold:
            self.buy()
            self.in_position = True

        # Sell condition: near top or rsi overbought
        near_top = self.data.close[0] >= self.box_top[0] * (1 - self.params.near_threshold)
        overbought = self.rsi[0] > self.params.rsi_overbought

        if self.in_position and (near_top or overbought):
            self.sell()
            self.in_position = False


def backtest_stuck_in_a_box(data_filepath: str, initial_cash: float = 10000.0) -> float:
    """
    Convenience function to backtest 'Stuck in a Box'.
    """
    return run_backtest(StuckInABoxStrategy, data_filepath, initial_cash)

# # Optional: if run standalone
# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("--data", type=str, default="data/solusd_1h.csv")
#     args = parser.parse_args()

#     final_value = backtest_stuck_in_a_box(args.data, 10000.0)
#     print(f"Final Portfolio Value: {final_value:.2f}")
