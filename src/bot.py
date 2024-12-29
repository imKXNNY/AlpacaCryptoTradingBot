# file: src/bot.py

import os
import logging
import pandas as pd
import alpaca_trade_api as tradeapi

# Local imports
from src.utils.data_fetch import fetch_ohlcv
from src.utils.risk_management import position_size, atr_stop_loss
from src.strategies.catch_the_wave import (
    catch_the_wave_signals,
    catch_the_wave_exit,
)
from src.strategies.stuck_in_a_box import (
    stuck_in_a_box_signals,
    stuck_in_a_box_exit,
)

# ========== Logging Configuration ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ========== Alpaca API Setup ==========
API_KEY = os.getenv("ALPACA_API_KEY", "Your-API-Key")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "Your-Secret-Key")
BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version="v2")


def run_strategy(
    symbol: str,
    strategy_type: str = "catch_the_wave",
    timeframe: str = "1Hour",
    lookback: int = 200,
    account_balance: float = 10000.0,  # Example balance
    risk_percent: float = 0.01,
    atr_multiplier: float = 1.5,
):
    """
    Orchestrates:
    1) Data fetching from Alpaca
    2) Strategy signal generation
    3) Risk-based position sizing & ATR stop-loss
    4) Order execution via Alpaca

    :param symbol: e.g. "BTCUSD" or "SOLUSD"
    :param strategy_type: "catch_the_wave" or "stuck_in_a_box"
    :param timeframe: e.g. "1Hour", "4Hour"
    :param lookback: how many bars to fetch
    :param account_balance: your current account size
    :param risk_percent: fraction of account to risk per trade
    :param atr_multiplier: multiplier for ATR-based stop-loss
    """

    # 1. Fetch Data
    df = fetch_ohlcv(symbol, timeframe=timeframe, limit=lookback)
    if df.empty:
        logging.warning(f"No data returned for {symbol}. Aborting.")
        return

    # 2. Generate Strategy Signals
    if strategy_type == "catch_the_wave":
        df = catch_the_wave_signals(df)
        df = catch_the_wave_exit(df)
    elif strategy_type == "stuck_in_a_box":
        df = stuck_in_a_box_signals(df)
        df = stuck_in_a_box_exit(df)
    else:
        logging.error(f"Unknown strategy_type: {strategy_type}")
        return

    # Identify latest bar signals
    latest_row = df.iloc[-1]
    signal = latest_row.get("signal", 0)
    exit_signal = latest_row.get("exit_signal", 0)

    logging.info(f"Strategy = {strategy_type}, Symbol = {symbol}, Signal = {signal}, Exit = {exit_signal}")

    if signal == 1:
        # 3A. ATR-based stop-loss (optional)
        atr = df["atr"].iloc[-1] if "atr" in df.columns else None
        if atr is None:
            # If we haven't explicitly calculated ATR yet, let's do it quickly
            import ta
            df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
            atr = df["atr"].iloc[-1]

        current_price = latest_row["close"]
        stop_loss_price = atr_stop_loss(current_price, atr, multiplier=atr_multiplier)

        # 3B. Position Sizing
        # (Entry Price - Stop Loss Price) must be > 0
        if current_price <= stop_loss_price:
            logging.warning("Stop loss is above or equal to current price. No trade.")
            return

        size = position_size(
            account_balance,
            risk_percent,
            entry_price=current_price,
            stop_loss_price=stop_loss_price,
        )
        if size <= 0:
            logging.warning("Calculated position size <= 0. No trade.")
            return

        # 4A. Place a Buy Order
        logging.info(f"Placing BUY order for {symbol} with size={size:.5f} at ~{current_price:.2f} stop_loss={stop_loss_price:.2f}")
        place_order(symbol, side="buy", qty=size)

    elif exit_signal == 1:
        # 4B. Place a Sell Order
        # Usually you'd check if we hold any position first
        position = get_open_position(symbol)
        if position and float(position.qty) > 0:
            qty = float(position.qty)
            logging.info(f"Placing SELL order for {symbol} with qty={qty} to exit position.")
            place_order(symbol, side="sell", qty=qty)
        else:
            logging.info(f"No open position to sell for {symbol}.")

    else:
        logging.info(f"No new action for {symbol} at this bar.")


def place_order(symbol: str, side: str, qty: float, order_type="market", time_in_force="gtc"):
    """
    Places an order via Alpaca's API.
    :param symbol: "BTCUSD", "SOLUSD", etc.
    :param side: "buy" or "sell"
    :param qty: quantity to trade
    :param order_type: default "market"
    :param time_in_force: "gtc", "day", etc.
    """
    try:
        # NOTE: For crypto, Alpaca allows fractional quantities, e.g. 0.001 BTC
        order = api.submit_order(
            symbol=symbol,
            side=side,
            type=order_type,
            qty=qty,
            time_in_force=time_in_force,
        )
        logging.info(f"Order submitted: {order}")
    except Exception as e:
        logging.error(f"Error placing {side.upper()} order for {symbol}: {e}")


def get_open_position(symbol: str):
    """
    Returns the open position for the specified symbol, or None if no position.
    """
    try:
        positions = api.list_positions()
        for pos in positions:
            if pos.symbol == symbol:
                return pos
        return None
    except Exception as e:
        logging.error(f"Error fetching positions: {e}")
        return None


def main():
    """
    Example usage of run_strategy(). 
    Adjust parameters to your needs.
    """
    # Single run for BTC/USD using "Catch the Wave" on 1Hour timeframe
    run_strategy(
        symbol="BTCUSD",
        strategy_type="catch_the_wave",
        timeframe="1Hour",
        lookback=200,    # how many bars
        account_balance=10000.0,
        risk_percent=0.01,
        atr_multiplier=1.5,
    )

    # If you also want to run "Stuck in a Box" for SOL:
    run_strategy(
        symbol="SOLUSD",
        strategy_type="stuck_in_a_box",
        timeframe="1Hour",
        lookback=200,
        account_balance=10000.0,
        risk_percent=0.02,  # example per the doc: we risk 2% for SOL
        atr_multiplier=1.5,
    )


if __name__ == "__main__":
    main()
