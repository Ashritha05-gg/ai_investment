import yfinance as yf
import numpy as np


def analyze_risk(symbol: str):
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")

    if df.empty:
        return None

    # Calculate daily returns
    df["Returns"] = df["Close"].pct_change()

    volatility = np.std(df["Returns"]) * np.sqrt(252)

    # Simple risk classification
    if volatility < 0.2:
        risk_level = "Low"
    elif volatility < 0.4:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return {
        "volatility": round(float(volatility), 4),
        "risk_level": risk_level,
    }
