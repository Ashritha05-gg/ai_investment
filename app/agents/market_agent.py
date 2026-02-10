# # import yfinance as yf
# # import pandas as pd
# # import pandas_ta as ta


# # def analyze_market(symbol: str):
# #     try:
# #         stock = yf.Ticker(symbol)

# #         # ===============================
# #         # 1 YEAR DATA (For Indicators)
# #         # ===============================
# #         df = stock.history(period="1y")

# #         if df.empty:
# #             return None

# #         # Technical Indicators
# #         df["SMA_20"] = ta.sma(df["Close"], length=20)
# #         df["RSI_14"] = ta.rsi(df["Close"], length=14)

# #         latest = df.iloc[-1]

# #         # ===============================
# #         # LAST 3 MONTHS (For Chart)
# #         # ===============================
# #         df_3m = stock.history(period="3mo")

# #         if df_3m.empty:
# #             return None

# #         df_3m["SMA_20"] = ta.sma(df_3m["Close"], length=20)

# #         price_history = []

# #         for index, row in df_3m.iterrows():
# #             # Skip rows where SMA is not ready yet
# #             if pd.notna(row["SMA_20"]):
# #                 price_history.append({
# #                     "date": index.strftime("%Y-%m-%d"),
# #                     "close": round(float(row["Close"]), 2),
# #                     "sma_20": round(float(row["SMA_20"]), 2),
# #                 })

# #         return {
# #             "symbol": symbol,
# #             "current_price": round(float(latest["Close"]), 2),
# #             "sma_20": round(float(latest["SMA_20"]), 2),
# #             "rsi_14": round(float(latest["RSI_14"]), 2),
# #             "price_history": price_history,
# #         }

# #     except Exception as e:
# #         print(f"Error analyzing market: {e}")
# #         return None




# import yfinance as yf
# import pandas as pd
# import pandas_ta as ta


# def analyze_market(symbol: str):
#     try:
#         stock = yf.Ticker(symbol)

#         # Fetch 1 year data for indicators
#         df = stock.history(period="1y")

#         if df.empty:
#             return None

#         # Technical indicators
#         df["SMA_20"] = ta.sma(df["Close"], length=20)
#         df["RSI_14"] = ta.rsi(df["Close"], length=14)

#         latest = df.iloc[-1]

#         current_price = round(float(latest["Close"]), 2)
#         sma_20 = round(float(latest["SMA_20"]), 2)
#         rsi_14 = round(float(latest["RSI_14"]), 2)

#         # -------- Portfolio Simulation --------
#         investment_amount = 100000  # ₹1 Lakh default

#         shares = investment_amount // current_price
#         invested_value = shares * current_price

#         # Assume buying 3 months ago
#         df_3m = stock.history(period="3mo")
#         if not df_3m.empty:
#             buy_price = round(float(df_3m.iloc[0]["Close"]), 2)
#         else:
#             buy_price = current_price

#         portfolio_value = round(shares * current_price, 2)
#         initial_value = round(shares * buy_price, 2)

#         profit_loss = round(portfolio_value - initial_value, 2)

#         if initial_value != 0:
#             profit_loss_percent = round((profit_loss / initial_value) * 100, 2)
#         else:
#             profit_loss_percent = 0

#         # -------- Price History (3 Months Chart) --------
#         df_3m["SMA_20"] = ta.sma(df_3m["Close"], length=20)

#         price_history = []

#         for index, row in df_3m.iterrows():
#             price_history.append({
#                 "date": index.strftime("%Y-%m-%d"),
#                 "close": round(float(row["Close"]), 2),
#                 "sma_20": round(
#                     float(row["SMA_20"]) if not pd.isna(row["SMA_20"]) else 0,
#                     2
#                 ),
#             })

#         return {
#             "symbol": symbol,
#             "current_price": current_price,
#             "sma_20": sma_20,
#             "rsi_14": rsi_14,
#             "price_history": price_history,
#             "portfolio": {
#                 "investment_amount": investment_amount,
#                 "shares": int(shares),
#                 "buy_price_3m_ago": buy_price,
#                 "current_value": portfolio_value,
#                 "profit_loss": profit_loss,
#                 "profit_loss_percent": profit_loss_percent,
#             }
#         }

#     except Exception:
#         return None



import yfinance as yf
import pandas as pd
import pandas_ta as ta


def analyze_market(symbol: str, period: str = "3mo", investment: float = 100000):
    try:
        stock = yf.Ticker(symbol)

        # Fetch full 1Y data for indicators
        df_full = stock.history(period="1y")

        if df_full.empty:
            return None

        df_full["SMA_20"] = ta.sma(df_full["Close"], length=20)
        df_full["RSI_14"] = ta.rsi(df_full["Close"], length=14)

        latest = df_full.iloc[-1]

        # ---- Fetch selected period data for simulation ----
        df_period = stock.history(period=period)

        if df_period.empty:
            return None

        buy_price = float(df_period["Close"].iloc[0])
        current_price = float(df_period["Close"].iloc[-1])

        shares = investment / buy_price
        current_value = shares * current_price
        profit_loss = current_value - investment
        return_percent = (profit_loss / investment) * 100

        # ---- Price history for chart ----
        df_period["SMA_20"] = ta.sma(df_period["Close"], length=20)

        price_history = []

        for index, row in df_period.iterrows():
            price_history.append({
                "date": index.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "sma_20": round(float(row["SMA_20"]) if not pd.isna(row["SMA_20"]) else 0, 2),
            })

        return {
            "symbol": symbol,
            "current_price": round(float(latest["Close"]), 2),
            "sma_20": round(float(latest["SMA_20"]), 2),
            "rsi_14": round(float(latest["RSI_14"]), 2),
            "price_history": price_history,

            # 🧮 Simulation Results
            "simulation": {
                "investment": investment,
                "buy_price": round(buy_price, 2),
                "current_value": round(current_value, 2),
                "profit_loss": round(profit_loss, 2),
                "return_percent": round(return_percent, 2),
                "shares": int(shares),
                "period": period,
            }
        }

    except Exception:
        return None
