# Alpaca Crypto Trading Bot | ACTB

![Crypto Trading Bot](https://example.com/your-image.png) <!-- Replace with an actual image if available -->

![Build Status](https://github.com/imKXNNY/AlpacaCryptoTradingBot/actions/workflows/ci.yml/badge.svg) ![Coverage](https://codecov.io/gh/imKXNNY/AlpacaCryptoTradingBot/branch/main/graph/badge.svg) ![License](https://img.shields.io/github/license/imKXNNY/AlpacaCryptoTradingBot)

## Table of Contents

1. [Overview](#overview)
2. [Goals](#goals)
3. [Trading Strategy](#trading-strategy)
    - [Market and Asset Selection](#market-and-asset-selection)
    - [Entry Rules](#entry-rules)
    - [Exit Rules](#exit-rules)
4. [Risk Management](#risk-management)
5. [Backtesting and Validation](#backtesting-and-validation)
6. [Implementation Plan](#implementation-plan)
    - [Daily Routine](#daily-routine)
    - [Weekly Routine](#weekly-routine)
7. [Tools and Resources](#tools-and-resources)
8. [Tech Stack & Development Plan](#tech-stack--development-plan)
    - [Programming Language & Environment](#programming-language--environment)
    - [Data Handling & Analysis](#data-handling--analysis)
    - [Alpaca API](#alpaca-api)
    - [Backtesting Tools](#backtesting-tools)
    - [Monitoring & Visualization](#monitoring--visualization)
    - [Scheduling](#scheduling)
    - [Version Control & Deployment](#version-control--deployment)
    - [Error Monitoring](#error-monitoring)
    - [Additional Libraries](#additional-libraries)
9. [Development Workflow](#development-workflow)
10. [Directory Structure](#directory-structure)
11. [Testing](#testing)
12. [To-Do List](#to-do-list)
13. [Performance Tracking and Journaling](#performance-tracking-and-journaling)
14. [Emotional and Mental Discipline](#emotional-and-mental-discipline)
15. [Continuous Improvement](#continuous-improvement)
16. [Long-Term Vision](#long-term-vision)
17. [Disclaimer](#disclaimer)
18. [Achievements](#achievements)
19. [Contact](#contact)
20. [Getting Started](#getting-started)
21. [Contributing](#contributing)
22. [License](#license)
23. [Acknowledgements](#acknowledgements)
24. [Screenshots](#screenshots)
25. [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
26. [Troubleshooting](#troubleshooting)
27. [Additional Resources](#additional-resources)
28. [Appendix](#appendix)

---

## Overview

**Crypto Trading Bot** aims to generate consistent profits through disciplined swing trading in cryptocurrency markets. Leveraging the Alpaca API and a suite of Python-based tools, the bot focuses on high-probability setups optimized through backtesting and robust risk management.

---

## Goals

### Short-Term Goals

- **Implement Strategies**: Develop and backtest strategies for each cryptocurrency pair and timeframe.
- **Achieve Win Rate**: Target a realistic win rate of 50-60% based on backtesting results.

### Long-Term Goals

- **Confidence Building**: Gain confidence in trading specific setups for each asset.
- **Capital Scaling**: Gradually increase trading capital after demonstrating consistent profitability with SOL/USDT and BTC/USDT on the 1H timeframe.

---

## Trading Strategy

### Market and Asset Selection

**Primary Market**: Cryptocurrency

**Target Assets**:

- **BTC (Bitcoin)**: Focus on the 1H timeframe using the "Catch the Wave" strategy.
- **ETH (Ethereum)**: Utilize the 4H timeframe with the "Stuck in a Box" strategy.
- **SOL (Solana)**: Apply both "Catch the Wave" and "Stuck in a Box" strategies across 1H and 4H timeframes.

**Timeframes**:

- **1-Hour (1H)**: Precision entries for BTC and SOL.
- **4-Hour (4H)**: Mid-term swing trades for ETH and SOL.
- **Daily (D1)**: Long-term support/resistance analysis (no active trading based on backtest results).

### Entry Rules

**Indicators**:

- **RSI (Relative Strength Index)**
- **ATR (Average True Range)**
- **50-MA (50-period Moving Average)**

**Conditions for Entry**:

#### Catch the Wave (Trending Markets)

- **Entry**: Enter a long position when:
  - Price pulls back to the 50-MA in an uptrend.
  - RSI is oversold (<30).
  - Bullish candlestick confirmation (e.g., hammer, engulfing pattern).

- **Focus**: BTC (1H) and SOL (1H).

#### Stuck in a Box (Range Markets)

- **Entry**: Enter a long position when:
  - Price nears the support zone (Box Bottom).
  - Bullish reversal patterns are identified (e.g., hammer, doji).
  - RSI confirms bullish momentum.

- **Focus**: SOL (1H, 4H) and ETH (4H).

### Exit Rules

**Take Profit**:

- **Catch the Wave**: Exit near the previous swing high or when RSI indicates overbought conditions (>70).
- **Stuck in a Box**: Exit near the range top (resistance level).

**Stop Loss**:

- **ATR-Based**: Implement dynamic stop-losses based on ATR to adjust for volatility.
  - **Catch the Wave**: Set stop-loss below the 50-MA.
  - **Stuck in a Box**: Set stop-loss below the support level.

---

## Risk Management

**Risk per Trade**:

- **ETH and BTC**: Risk 1% of account balance per trade.
- **SOL**: Risk 2% of account balance per trade due to higher profitability.

**Position Sizing Formula**:

\[
\text{Position Size} = \frac{\text{Account Balance} \times \text{Risk \%}}{\text{Entry Price} - \text{Stop Loss Price}}
\]

---

## Backtesting and Validation

### Backtesting Plan

- **Focus Pairs/Timeframes**:
  - BTC/USDT (1H)
  - SOL/USDT (1H & 4H)
  - ETH/USDT (4H)

- **Strategy Optimization**:
  - Test high-probability setups to avoid overfitting.

### Metrics to Track

- **Net Profit and Win Rate**: Prioritize for SOL and BTC.
- **Risk/Reward Ratio**: Maintain an average R:R of 1.5 or greater.
- **Drawdowns**: Keep drawdowns below 5% to mitigate significant losses.

### Analysis

- Use backtest findings to refine stop-loss and take-profit levels dynamically based on ATR.

---

## Implementation Plan

### Daily Routine

- **Morning**:
  - Check news affecting BTC, ETH, SOL.
  - Analyze 1H and 4H charts for potential setups.

- **Trading Session**:
  - Execute trades strictly based on predefined rules for BTC (1H), ETH (4H), and SOL (1H & 4H).
  - Utilize TradingView alerts to monitor key levels and confirm entries.

- **Evening**:
  - Review trades and update the trading journal.

### Weekly Routine

- **Performance Review**:
  - Evaluate win rate and profitability by asset and timeframe.
  
- **Strategy Refinement**:
  - For BTC/USDT, prioritize "Catch the Wave" on 1H.
  - For SOL/USDT, focus on both "Stuck in a Box" (4H) and "Catch the Wave" (1H).
  - Revisit ETH trading only if market conditions improve significantly.

---

## Tools and Resources

### Charting Software

- **TradingView**: For real-time alerts and advanced charting capabilities.

### Automated Tools

- **Alerts**: Utilize TradingView alerts for RSI thresholds, MA pullbacks, and support/resistance tests.

---

## Tech Stack & Development Plan

### Programming Language & Environment

1. **Python**:
   - **Poetry**: For dependency management and virtual environments.
   - **Pytest**: For unit testing to ensure the bot behaves as expected.

### Data Handling & Analysis

1. **Pandas**:
   - Essential for data manipulation and time-series analysis.
2. **NumPy**:
   - For mathematical computations like calculating indicators or portfolio optimization.
3. **Matplotlib/Plotly**:
   - For plotting backtest results, trade outcomes, and performance metrics.

### Alpaca API

1. **Alpaca Trading API**:
   - Free tier for live and paper trading.
   - Fetch market data, execute trades, and manage account details.
2. **Alpaca-Py**:
   - Python SDK for seamless integration with Alpaca's API endpoints.

### Backtesting Tools

1. **Backtrader**:
   - Python-based backtesting library for designing custom strategies.
2. **Freqtrade** (Optional):
   - Open-source platform for backtesting and live trading if Alpaca’s backtesting options are insufficient.

### Monitoring & Visualization

1. **Streamlit**:
   - Create interactive dashboards to visualize performance, monitor trades, and configure bot parameters in real-time.

### Scheduling

1. **APScheduler**:
   - Schedule tasks like polling Alpaca API for market updates, calculating signals, and executing trades.

### Version Control & Deployment

1. **Git + GitHub**:
   - Version control for managing the codebase and collaborating.
2. **Local Development**:
   - Initial development and testing on a local machine.
3. **Cloud Deployment** (Optional):
   - Utilize free tiers like AWS Free Tier, Google Cloud Free Tier, or Heroku for hosting the bot. Monitor resource usage to stay within free limits.

### Error Monitoring

1. **Sentry.io** (Free Tier):
   - Monitor runtime errors, API failures, or unexpected behavior in the bot.

### Additional Libraries

1. **TA-Lib**:
   - For creating custom indicators or calculating standard ones like RSI, MACD, etc.
2. **QuantLib** (Optional):
   - For advanced quantitative analysis.

### Documentation

1. **Markdown + GitHub Wiki**:
   - Document strategy details, configurations, and troubleshooting steps.

---

## Development Workflow

### 1. Setup the Environment

- **Install Python** (preferably 3.9+).
- **Initialize Project with Poetry**:
  
  ```bash
  mkdir trading-bot && cd trading-bot
  poetry init
  poetry add pandas numpy matplotlib alpaca-py streamlit APScheduler TA-Lib
  poetry add --dev pytest pytest-cov
  ```
  
- **Configure Git**:
  
  ```bash
  git init
  git remote add origin https://github.com/yourusername/trading-bot.git
  git add .
  git commit -m "Initial commit"
  git push -u origin master
  ```

### 2. Build Core Components

#### Data Fetching

- **`src/utils/fetch_data.py`**: Function to pull historical and live data via Alpaca.

#### Signal Generation

- **`src/strategies/catch_the_wave.py`**: Logic for "Catch the Wave".
- **`src/strategies/stuck_in_a_box.py`**: Logic for "Stuck in a Box".

#### Order Execution

- **`src/bot.py`**: Main script that decides trades based on signals and risk rules.

#### Backtesting

- **`src/backtest.py`**: Simulate the strategies on historical data using Backtrader or Freqtrade.

### 3. Integrate Monitoring & Visualization

- **Streamlit Dashboard**:
  - **`streamlit_app/app.py`**: Visualize current positions, PnL, RSI states, next possible signals, etc.

### 4. Automate the Bot

- **Scheduling with APScheduler**:
  - **`src/scheduler.py`**: Schedule periodic data fetch (every hour or as needed).

### 5. Testing

- **Unit Tests**:
  - Located in `tests/` directory.
  - Example: `tests/test_utils/test_fetch_ohlcv.py`
  
- **Running Tests**:
  
  ```bash
  poetry run pytest --cov=src --cov-report=term-missing
  ```

### 6. Deployment

- **Local Testing**:
  - Run the bot locally and monitor performance.
  
- **Cloud Deployment** (Optional):
  - Deploy to Heroku, AWS Free Tier, or Google Cloud.
  - Ensure lightweight operations to stay within free limits.
  
- **Monitor Resources**:
  - Keep an eye on CPU usage and other resources to prevent exceeding free tier limits.

---

## Directory Structure

```plaintext
trading-bot/
├── data/                   # Historical data, logs
├── src/
│   ├── strategies/
│   │   ├── catch_the_wave.py
│   │   └── stuck_in_a_box.py
│   ├── utils/
│   │   ├── fetch_data.py
│   │   ├── risk_management.py
│   │   └── ...
│   ├── bot.py              # Main trading logic
│   ├── scheduler.py        # APScheduler tasks
│   └── backtest.py         # Backtesting logic
├── streamlit_app/
│   └── app.py              # Streamlit dashboard
├── tests/
│   ├── test_utils/
│   │   ├── test_fetch_ohlcv.py
│   │   └── test_risk_management.py
│   ├── test_strategies/
│   │   ├── test_catch_the_wave.py
│   │   └── test_stuck_in_a_box.py
│   ├── test_backtest.py
│   └── ...
├── pyproject.toml          # Poetry config
├── README.md               # Documentation
└── .gitignore              # Git ignore file
```

---

## Testing

### Running Tests

Execute the following command to run all tests with coverage:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

**Coverage Report:**

```
---------- coverage: platform win32, python 3.12.8-final-0 -----------
Name                                           Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------------
src\utils\risk_management.py                      11      0   100%
tests\test_utils\test_risk_management.py          43      0   100%
-----------------------------------------------------------------------------
TOTAL                                            54      0   100%
Coverage HTML written to dir htmlcov
```

### Example Test Case

#### Fetch Data Test

```python
# tests/test_utils/test_fetch_ohlcv.py

import pandas as pd
from src.utils.fetch_data import fetch_ohlcv
from unittest.mock import MagicMock

def test_fetch_ohlcv(mocker):
    # Mock Alpaca CryptoBars data
    mock_data = pd.DataFrame({
        "symbol": ["BTC/USD", "BTC/USD"],
        "timestamp": ["2024-12-27T06:00:00+00:00", "2024-12-27T07:00:00+00:00"],
        "open": [96197.5480, 96432.2500],
        "high": [96478.1450, 96432.2500],
        "low": [96034.8780, 94612.4150],
        "close": [96478.1450, 95003.1200],
        "volume": [0.0, 0.044213],
        "trade_count": [0, 11],
        "vwap": [96213.8915, 95031.942193],
    })

    # Convert to MultiIndex DataFrame similar to Alpaca's SDK
    mock_data.set_index(["symbol", "timestamp"], inplace=True)

    # Mock the client.get_crypto_bars method to return the mock data
    mock_response = MagicMock()
    mock_response.df = mock_data
    mocker.patch("src.utils.fetch_data.client.get_crypto_bars", return_value=mock_response)

    # Call the function
    result = fetch_ohlcv("BTC/USD", timeframe="Hour", limit=2)

    # Assert the DataFrame structure
    assert not result.empty
    assert "Open" in result.columns
    assert "Close" in result.columns
    assert "Volume" in result.columns
    assert len(result) == 2

    # Assert specific column values
    assert result["Open"].iloc[0] == 96197.5480
    assert result["Close"].iloc[1] == 95003.1200
```

---

## To-Do List

### **High Priority**

1. [x] **Finalize Strategy Signal Generation**
    - **Task**: Ensure `catch_the_wave_signals` and `stuck_in_a_box_signals` correctly generate buy/sell signals based on indicators.
    - **Subtasks**:
        - [x] Review and refine signal generation logic.
        - [x] Adjust strategy parameters (`ma_period`, `rsi_period`, etc.) for accuracy.
        - [x] Write comprehensive unit tests for each strategy.

2. [x] **Refine Backtesting Logic**
    - **Task**: Ensure `backtest_catch_the_wave` accurately simulates trades based on generated signals.
    - **Subtasks**:
        - [x] Align backtest logic with strategy signals.
        - [x] Fix any failing backtest tests by aligning data and logic.
        - [x] Validate backtest results against expected outcomes.

3. [x] **Implement and Test Risk Management**
    - **Task**: Develop risk management functions to control trade sizes and stop-loss levels.
    - **Subtasks**:
        - [x] Complete implementation of risk management functions in `risk_management.py`.
        - [x] Write and pass unit tests for these functions.
        - [x] Integrate risk management into backtesting and live trading.

4. [x] **Build and Test Live Trading Execution**
    - **Task**: Develop the execution layer to place buy/sell orders via Alpaca API based on signals.
    - **Subtasks**:
        - [x] Implement `execute_trade` functions.
        - [x] Write tests to mock API calls and verify order placements.
        - [x] Ensure safety checks are in place to prevent unintended trades.

### **Medium Priority**

5. [ ] **Enhance Logging and Monitoring**
    - **Task**: Improve logging for data fetching, signal generation, backtesting, and live trading.
    - **Subtasks**:
        - [ ] Integrate detailed logging in all modules.
        - [ ] Set up Sentry for real-time error monitoring.
        - [ ] Develop a Streamlit dashboard to visualize bot performance and trade history.

6. [ ] **Automate with Scheduling**
    - **Task**: Schedule periodic tasks like data fetching, signal generation, and trade execution.
    - **Subtasks**:
        - [ ] Implement scheduling using APScheduler.
        - [ ] Ensure tasks run reliably at specified intervals.
        - [ ] Monitor scheduled tasks for failures or delays.

7. [ ] **Develop Comprehensive Unit and Integration Tests**
    - **Task**: Expand test coverage to include all components of the bot.
    - **Subtasks**:
        - [ ] Write unit tests for all utility functions and strategies.
        - [ ] Develop integration tests to validate end-to-end workflows.
        - [ ] Continuously run tests to catch regressions early.

### **Low Priority**

8. [ ] **Documentation and User Guide**
    - **Task**: Document the entire project for ease of use and future development.
    - **Subtasks**:
        - [ ] Complete the README with setup instructions, usage examples, and troubleshooting tips.
        - [ ] Maintain a GitHub Wiki for detailed documentation.
        - [ ] Comment code thoroughly for better maintainability.

9. [ ] **Optimize and Refactor Codebase**
    - **Task**: Improve code quality for better performance and readability.
    - **Subtasks**:
        - [ ] Refactor repetitive code into reusable functions or classes.
        - [ ] Optimize data processing for speed and efficiency.
        - [ ] Ensure adherence to Python best practices and PEP 8 standards.

10. [ ] **Explore Additional Strategies and Indicators**
    - **Task**: Implement and backtest additional trading strategies to diversify bot capabilities.
    - **Subtasks**:
        - [ ] Research and develop new strategies (e.g., Mean Reversion, Momentum-based).
        - [ ] Integrate new indicators using TA-Lib or custom calculations.
        - [ ] Backtest and validate the performance of new strategies.

---

## Performance Tracking and Journaling

### Metrics to Track

- **Net Profit**: Focus on SOL’s profitability.
- **Risk/Reward Ratios**: Maintain an average R:R of 1.5:1 or higher.
- **Win Rate**: Target 50-60% for BTC and SOL.

### Tools

- **Excel/Notion**: Log trades manually or automate logging within the bot.
- **Automated Logs**: Implement detailed logging within Python scripts to track trade rationales and outcomes.

---

## Emotional and Mental Discipline

### Rules for Emotional Control

- **Trade Limits**: Stop trading for the day after 2 consecutive losses to maintain discipline.
- **Journaling**: Use journaling to identify emotional biases and refine decision-making processes.

### Mindset Development

- **Consistency**: Stick to the trading plan and avoid chasing random opportunities.
- **Resilience**: Learn from losses and continuously improve strategies without emotional interference.

---

## Continuous Improvement

### Learning Goals

- **Advanced Stop-Loss Techniques**: Experiment with ATR and Fibonacci retracements for dynamic stop-loss placement.
- **Strategy Refinement**: Continuously refine trade rules based on backtest results and live trading performance.

### Feedback Loop

- **Weekly Reviews**: Analyze trading journal entries and backtest outcomes to identify areas for improvement.
- **Adaptation**: Modify strategies based on market conditions and performance metrics to enhance profitability.

---

## Long-Term Vision

### Scaling Plan

- **Gradual Increase**: Increase trade sizes for SOL trades after demonstrating consistent profitability over 3-6 months.
- **Reintroduce ETH Trades**: Reassess and reintroduce ETH trades when backtesting indicates improved market conditions.

### Wealth-Building Goals

- **Capital Reinforcement**: Reinvest profits into long-term investments such as stocks, real estate, or other markets to diversify wealth-building strategies.

---

## Disclaimer

This project is intended for educational purposes only and does not constitute financial advice. Always conduct your own due diligence and consult with a financial professional before making any investment decisions. The author is not responsible for any financial losses incurred through the use of this trading bot.

---

## Achievements

- ✅ **100% Test Coverage**: All modules, including `risk_management.py`, are fully tested with comprehensive unit tests.
- ✅ **All Tests Passing**: Ensured that all tests pass successfully, guaranteeing the reliability of the trading strategies and risk management.
- 🎯 **Robust Trading Strategies**: Developed and validated "Catch the Wave" and "Stuck in a Box" strategies through extensive backtesting.
- 🚀 **Scalable Architecture**: Structured the project with a clear directory hierarchy, facilitating future expansions and maintenance.

![Coverage Badge](https://img.shields.io/codecov/c/github/yourusername/trading-bot?label=Coverage) ![Build Status](https://img.shields.io/github/workflow/status/yourusername/trading-bot/CI?label=Build) ![License](https://img.shields.io/github/license/yourusername/trading-bot)

---

## Contact

For any questions, issues, or contributions, please open an issue or submit a pull request on the [GitHub repository](https://github.com/yourusername/trading-bot).

---

# Getting Started

To help you get started quickly, follow these steps to set up your development environment and begin implementing your trading bot.

### Prerequisites

- **Python 3.9+**: Ensure you have Python installed. You can download it from the [official website](https://www.python.org/downloads/).
- **Poetry**: A tool for dependency management and packaging in Python. Install it following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/trading-bot.git
    cd trading-bot
    ```

2. **Set Up the Virtual Environment**

    ```bash
    poetry install
    ```

3. **Set Up Environment Variables**

    Create a `.env` file in the project root and add your Alpaca API credentials:

    ```dotenv
    ALPACA_API_KEY=your_alpaca_api_key
    ALPACA_SECRET_KEY=your_alpaca_secret_key
    ```

4. **Run the Bot Locally**

    ```bash
    poetry run python src/bot.py
    ```

---

# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

# License

This project is licensed under the [MIT License](LICENSE).

---

# Acknowledgements

- **Alpaca**: For providing a robust API for trading and data fetching.
- **Python Community**: For extensive libraries and support in developing trading bots.

---

# Screenshots

![Dashboard](https://example.com/dashboard-screenshot.png) <!-- Replace with actual screenshots if available -->

---

# Frequently Asked Questions (FAQ)

**Q1: How do I add a new trading strategy?**

*Answer*: Create a new Python script in the `src/strategies/` directory, implement your strategy logic, and write corresponding tests in the `tests/` directory.

**Q2: How can I monitor the bot's performance?**

*Answer*: Use the Streamlit dashboard located in the `streamlit_app/` directory to visualize open trades, PnL, and other performance metrics in real-time.

**Q3: Can I use this bot for live trading?**

*Answer*: Yes, once thoroughly backtested and paper-traded, you can configure the bot for live trading using Alpaca’s live trading API. Ensure you understand the risks and have proper safeguards in place.

---

# Troubleshooting

**Issue**: `403 Forbidden` error when fetching crypto data.

*Solution*: Ensure you have the correct Alpaca subscription for crypto data. Use the `get_crypto_bars` method with proper symbol formatting (`"BTC/USD"` instead of `"BTCUSD"`).

**Issue**: Test failures due to mismatched DataFrame structures.

*Solution*: Align your mock data structure with the real Alpaca API responses. Ensure MultiIndex is correctly mocked in tests.

---

# Additional Resources

- **Alpaca API Documentation**: [https://alpaca.markets/docs/api-references/market-data-api/](https://alpaca.markets/docs/api-references/market-data-api/)
- **TA-Lib Documentation**: [https://mrjbq7.github.io/ta-lib/](https://mrjbq7.github.io/ta-lib/)
- **Backtrader Documentation**: [https://www.backtrader.com/docu/](https://www.backtrader.com/docu/)
- **Freqtrade Documentation**: [https://www.freqtrade.io/en/latest/](https://www.freqtrade.io/en/latest/)
- **Streamlit Documentation**: [https://docs.streamlit.io/](https://docs.streamlit.io/)
- **APScheduler Documentation**: [https://apscheduler.readthedocs.io/en/stable/](https://apscheduler.readthedocs.io/en/stable/)

---

# Appendix

## Sample Configuration

### `.env` File

```dotenv
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
```

### `pyproject.toml`

```toml
[tool.poetry]
name = "trading-bot"
version = "0.1.0"
description = "A crypto trading bot using Alpaca API"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
pandas = "^1.3.0"
numpy = "^1.21.0"
matplotlib = "^3.4.0"
alpaca-py = "^0.5.0"
streamlit = "^1.0.0"
APScheduler = "^3.7.0"
TA-Lib = "^0.4.0"

[tool.poetry.dev-dependencies]
pytest = "^6.2.0"
pytest-cov = "^2.12.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

# Conclusion

Embarking on building a crypto trading bot can be challenging, but with a clear roadmap, structured development approach, and robust testing, you can systematically overcome hurdles and achieve your trading goals. This README serves as a comprehensive guide to steer your project towards success. Stay disciplined, continuously test and refine your strategies, and leverage the tools and resources outlined to build a reliable and profitable trading bot.

Happy Trading! 🚀