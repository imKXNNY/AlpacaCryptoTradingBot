# file: src/backtest.py
import pandas as pd
from strategies.catch_the_wave import catch_the_wave_signals, catch_the_wave_exit
from strategies.stuck_in_a_box import stuck_in_a_box_signals, stuck_in_a_box_exit

def backtest_catch_the_wave(df: pd.DataFrame):
    # Generate signals
    df = catch_the_wave_signals(df)
    df = catch_the_wave_exit(df)

    # Very simplified PnL calculation:
    #  - 'signal' = 1 -> buy next bar open
    #  - 'exit_signal' = 1 -> sell next bar open
    # Keep track of one position at a time
    balance = 1000.0
    in_position = False
    entry_price = 0.0
    
    for i in range(len(df) - 1):
        if df.loc[df.index[i], "signal"] == 1 and not in_position:
            # Buy next bar open
            entry_price = df["Open"].iloc[i+1]
            in_position = True
        elif df.loc[df.index[i], "exit_signal"] == 1 and in_position:
            # Sell next bar open
            exit_price = df["Open"].iloc[i+1]
            # PnL calc
            pct_change = (exit_price - entry_price) / entry_price
            balance *= (1 + pct_change)
            in_position = False
    
    # If still in position at the end, sell at final close
    if in_position:
        final_close = df["Close"].iloc[-1]
        pct_change = (final_close - entry_price) / entry_price
        balance *= (1 + pct_change)
    
    return balance
