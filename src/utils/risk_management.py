# file: src/utils/risk_management.py
def position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
) -> float:
    """
    Position Size = (Account Balance * Risk %) / (Entry Price - Stop Loss Price)
    """
    risk_amount = account_balance * risk_percent
    # Avoid division by zero
    diff = entry_price - stop_loss_price
    if diff <= 0:
        return 0.0
    size = risk_amount / diff
    return round(size, 4)  # or however you want to format


def atr_stop_loss(
    current_price: float, atr_value: float, multiplier: float = 1.5
) -> float:
    """
    Example: Stop loss below current_price by a multiple of ATR.
    """
    return current_price - (atr_value * multiplier)
