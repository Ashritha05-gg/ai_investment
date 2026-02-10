import yfinance as yf
import pandas_ta as ta
import numpy as np


def analyze_market_regime():
    nifty = yf.download("^NSEI", period="6mo", interval="1d", auto_adjust=True)

    if nifty.empty or len(nifty) < 50:
        return {"regime": "Unknown"}

    # Handle possible multi-index columns
    if isinstance(nifty.columns, type(nifty.columns)) and len(nifty.columns.names) > 1:
        nifty.columns = nifty.columns.get_level_values(0)

    nifty["SMA_50"] = ta.sma(nifty["Close"], length=50)
    nifty["RSI_14"] = ta.rsi(nifty["Close"], length=14)

    latest_row = nifty.iloc[-1]

    price = latest_row["Close"]
    sma_50 = latest_row["SMA_50"]
    rsi = latest_row["RSI_14"]

    if pd_is_invalid(price) or pd_is_invalid(sma_50) or pd_is_invalid(rsi):
        return {"regime": "Unknown"}

    price = float(price)
    sma_50 = float(sma_50)
    rsi = float(rsi)

    if price > sma_50 and rsi > 50:
        regime = "Bullish"
    elif price < sma_50 and rsi < 50:
        regime = "Bearish"
    else:
        regime = "Neutral"

    return {
        "nifty_price": round(price, 2),
        "sma_50": round(sma_50, 2),
        "rsi_14": round(rsi, 2),
        "regime": regime,
    }


def pd_is_invalid(value):
    try:
        return np.isnan(value)
    except:
        return False
