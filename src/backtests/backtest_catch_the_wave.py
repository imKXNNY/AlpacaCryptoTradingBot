# File: src/backtests/backtest_catch_the_wave.py
# Description: Implement a simple backtest using the CatchTheWave strategy.

import backtrader as bt
from backtests.backtest_shared import run_backtest

class CatchTheWaveStrategy(bt.Strategy):
    params = {
        "ma_period": 50,
        "rsi_period": 14,
        "rsi_oversold": 55,
        "rsi_overbought": 75
    }

    def __init__(self):
        self.ma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma_period)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.in_position = False

    def next(self):
        # Log current data and indicator values
        self.log(f"Close: {self.data.close[0]}, MA50: {self.ma50[0]}, RSI: {self.rsi[0]}")

        # Simple uptrend check
        uptrend = self.data.close[0] > self.ma50[0]

        # Buy condition
        if not self.in_position and uptrend and (self.rsi[0] < self.params.rsi_oversold):
            self.buy()
            self.in_position = True
            self.log("BUY executed")

        # Sell condition
        elif self.in_position and (self.rsi[0] > self.params.rsi_overbought):
            self.sell()
            self.in_position = False
            self.log("SELL executed")

    def log(self, message):
        dt = self.data.datetime.datetime(0)
        print(f"{dt}: {message}")

def backtest_catch_the_wave(data_filepath: str, initial_cash: float = 10000.0) -> float:
    """
    Convenience function to backtest 'Catch the Wave'.
    """
    return run_backtest(CatchTheWaveStrategy, data_filepath, initial_cash)

# # Optional: if run standalone
# if __name__ == "__main__":
#     cerebro = bt.Cerebro()
#     data = bt.feeds.GenericCSVData(dataname="data/btcusd_1h.csv", dtformat="%Y-%m-%d %H:%M:%S")
#     cerebro.adddata(data)
#     cerebro.addstrategy(CatchTheWaveStrategy)
#     cerebro.broker.setcash(10000.0)

#     results = cerebro.run()
#     print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
#     cerebro.plot()
