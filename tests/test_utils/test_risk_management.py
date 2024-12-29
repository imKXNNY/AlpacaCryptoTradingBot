# tests/test_utils/test_risk_management.py

from src.utils.risk_management import position_size, atr_stop_loss


def test_position_size():
    """
    Test the position_size function with valid inputs where diff > 0.
    """
    # Scenario where diff > 0
    size = position_size(
        account_balance=10000, risk_percent=0.01, entry_price=100, stop_loss_price=95
    )
    assert size == 20.0  # (10000 * 0.01) / (100 - 95)


def test_position_size_diff_zero():
    """
    Test the position_size function when diff == 0.
    """
    # Scenario where diff == 0
    size = position_size(
        account_balance=10000, risk_percent=0.01, entry_price=100, stop_loss_price=100
    )
    assert size == 0.0  # Should return 0.0 when diff <= 0


def test_position_size_diff_negative():
    """
    Test the position_size function when diff < 0.
    """
    # Scenario where diff < 0
    size = position_size(
        account_balance=10000, risk_percent=0.01, entry_price=95, stop_loss_price=100
    )
    assert size == 0.0  # Should return 0.0 when diff <= 0


def test_atr_stop_loss():
    """
    Test the atr_stop_loss function with valid inputs.
    """
    stop_loss = atr_stop_loss(current_price=100, atr_value=5, multiplier=1.5)
    assert stop_loss == 92.5  # 100 - (5 * 1.5)


def test_atr_stop_loss_default_multiplier():
    """
    Test the atr_stop_loss function with default multiplier.
    """
    stop_loss = atr_stop_loss(current_price=150, atr_value=10)
    assert stop_loss == 135.0  # 150 - (10 * 1.5)


def test_atr_stop_loss_zero_atr():
    """
    Test the atr_stop_loss function when ATR value is zero.
    """
    stop_loss = atr_stop_loss(current_price=100, atr_value=0, multiplier=1.5)
    assert stop_loss == 100.0  # 100 - (0 * 1.5)


def test_atr_stop_loss_negative_atr():
    """
    Test the atr_stop_loss function when ATR value is negative.
    """
    stop_loss = atr_stop_loss(current_price=100, atr_value=-5, multiplier=1.5)
    assert stop_loss == 107.5  # 100 - (-5 * 1.5)


def test_position_size_invalid_inputs():
    """
    Test the position_size function with invalid inputs to ensure robustness.
    """
    # Negative account balance
    size = position_size(
        account_balance=-10000, risk_percent=0.01, entry_price=100, stop_loss_price=95
    )
    assert size == -20.0  # (-10000 * 0.01) / (100 - 95)

    # Risk percent greater than 1
    size = position_size(
        account_balance=10000, risk_percent=1.5, entry_price=100, stop_loss_price=95
    )
    assert size == 3000.0  # (10000 * 1.5) / (100 - 95)

    # Zero risk percent
    size = position_size(
        account_balance=10000, risk_percent=0.0, entry_price=100, stop_loss_price=95
    )
    assert size == 0.0  # (10000 * 0) / (100 - 95)


def test_atr_stop_loss_invalid_inputs():
    """
    Test the atr_stop_loss function with invalid inputs to ensure robustness.
    """
    # Negative multiplier
    stop_loss = atr_stop_loss(current_price=100, atr_value=5, multiplier=-1.5)
    assert stop_loss == 107.5  # 100 - (5 * -1.5)

    # Zero multiplier
    stop_loss = atr_stop_loss(current_price=100, atr_value=5, multiplier=0)
    assert stop_loss == 100.0  # 100 - (5 * 0)

    # Extremely high multiplier
    stop_loss = atr_stop_loss(current_price=100, atr_value=5, multiplier=10)
    assert stop_loss == 50.0  # 100 - (5 * 10)


def test_atr_stop_loss_large_values():
    """
    Test the atr_stop_loss function with very large values.
    """
    stop_loss = atr_stop_loss(current_price=1e6, atr_value=1e4, multiplier=2)
    assert stop_loss == 980000.0  # 1,000,000 - (10,000 * 2)


def test_atr_stop_loss_small_values():
    """
    Test the atr_stop_loss function with very small values.
    """
    stop_loss = atr_stop_loss(current_price=1.0, atr_value=0.1, multiplier=1.5)
    assert stop_loss == 0.85  # 1.0 - (0.1 * 1.5)
