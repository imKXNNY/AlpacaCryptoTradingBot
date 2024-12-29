# file: tests/conftest.py
import sys
import pytest
import pandas as pd
import os
from pathlib import Path

@pytest.fixture(scope="module")
def btcusdt_1h_data():
    filepath = os.path.join("tests", "tmp-data", "temp_cleaned_btcusdt_1h.csv")
    df = pd.read_csv(filepath)
    return df

# 
# NOT REQUIRED AS WE FOCUS ON BTC AND SOL CURRENTLY
# 
# @pytest.fixture(scope="module")
# def ethusdt_1h_data():
#     filepath = os.path.join("tests", "tmp-data", "temp_cleaned_ethusdt_1h.csv")
#     df = pd.read_csv(filepath)
#     return df

@pytest.fixture(scope="module")
def solusdt_1h_data():
    filepath = os.path.join("tests", "tmp-data", "temp_cleaned_solusdt_1h.csv")
    df = pd.read_csv(filepath)
    return df

# Add more fixtures as needed for other data files


# Add the `src` directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
