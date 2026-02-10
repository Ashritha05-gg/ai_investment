



# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware

# from app.agents.market_agent import analyze_market
# from app.agents.risk_agent import analyze_risk
# from app.agents.decision_agent import make_decision
# from app.agents.sentiment_agent import analyze_sentiment
# from app.agents.langchain_agent import run_langchain_agent
# from app.agents.market_regime_agent import analyze_market_regime


# app = FastAPI(title="AI Investment Decision Agent")


# # --------------------------------------------------
# # 🔐 CORS Configuration (for React frontend)
# # --------------------------------------------------

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Dev mode (restrict in production)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # --------------------------------------------------
# # 🏠 Root Endpoint
# # --------------------------------------------------

# @app.get("/")
# def home():
#     return {"message": "AI Investment Agent Running"}


# # --------------------------------------------------
# # 🤖 LangChain Multi-Agent Route
# # --------------------------------------------------

# @app.get("/langchain/{symbol}")
# def analyze_langchain(symbol: str):
#     """
#     Uses LangChain agent to dynamically orchestrate:
#     - Market tool
#     - Risk tool
#     - Sentiment tool
#     - Market regime tool

#     Returns LLM-driven decision.
#     """
#     return run_langchain_agent(symbol)


# # --------------------------------------------------
# # 🧠 Deterministic AI Decision Engine
# # --------------------------------------------------

# @app.get("/analyze/{symbol}")
# def analyze(
#     symbol: str,
#     period: str = Query("3mo", description="Historical period for chart"),
#     investment: float = Query(100000, description="Simulated investment amount")
# ):
#     """
#     Core AI Engine (non-LLM version)

#     Combines:
#     - Technical indicators
#     - Risk classification
#     - News sentiment
#     - Market regime

#     Uses rule-based scoring logic.
#     """

#     try:
#         market_data = analyze_market(symbol, period, investment)
#         risk_data = analyze_risk(symbol)
#         sentiment_data = analyze_sentiment(symbol)
#         market_regime = analyze_market_regime()

#         if not market_data or not risk_data:
#             return {"error": "Invalid stock symbol"}

#         decision = make_decision(
#             market_data=market_data,
#             risk_data=risk_data,
#             sentiment_data=sentiment_data,
#             market_regime=market_regime
#         )

#         return {
#             "engine": "deterministic",
#             "market_regime": market_regime,
#             "market_data": market_data,
#             "risk_data": risk_data,
#             "sentiment_data": sentiment_data,
#             "decision": decision,
#         }

#     except Exception as e:
#         return {
#             "error": "Analysis failed",
#             "details": str(e)
#         }





from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.agents.langchain_agent import run_langchain_agent

app = FastAPI(title="AI Investment Decision Agent (LangChain Core)")


# --------------------------------------------------
# 🔐 CORS Configuration (for React frontend)
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev mode (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 🏠 Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Investment Agent Running (LangChain Powered)"
    }


# --------------------------------------------------
# 🤖 MAIN ANALYSIS ROUTE (LangChain Core)
# --------------------------------------------------

@app.get("/analyze/{symbol}")
def analyze(
    symbol: str,
    period: str = Query("3mo", description="Historical period for chart"),
    investment: float = Query(100000, description="Simulated investment amount")
):
    """
    LangChain-driven Multi-Agent Investment Engine.

    Uses:
    - market_tool
    - risk_tool
    - sentiment_tool
    - regime_tool

    Returns LLM-based structured investment decision.
    """

    try:
        return run_langchain_agent(
            symbol=symbol,
            period=period,
            investment=investment
        )

    except Exception as e:
        return {
            "error": "LangChain analysis failed",
            "details": str(e)
        }
