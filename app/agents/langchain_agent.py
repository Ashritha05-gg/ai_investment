# # import json

# # from langchain_core.tools import tool
# # from langchain.agents import create_agent
# # from langchain_google_genai import ChatGoogleGenerativeAI

# # from app.agents.market_agent import analyze_market
# # from app.agents.risk_agent import analyze_risk
# # from app.agents.sentiment_agent import analyze_sentiment
# # from app.agents.market_regime_agent import analyze_market_regime
# # from app.config import GEMINI_API_KEY


# # # --------------------------------------------------
# # # 🔧 TOOL DEFINITIONS
# # # --------------------------------------------------

# # @tool
# # def market_tool(symbol: str) -> str:
# #     """
# #     Fetch stock technical indicators like current price, SMA, RSI,
# #     and price history.
# #     """
# #     data = analyze_market(symbol)
# #     return json.dumps(data)


# # @tool
# # def risk_tool(symbol: str) -> str:
# #     """
# #     Calculate stock volatility and classify risk level.
# #     """
# #     data = analyze_risk(symbol)
# #     return json.dumps(data)


# # @tool
# # def sentiment_tool(symbol: str) -> str:
# #     """
# #     Analyze recent news sentiment for a stock.
# #     """
# #     data = analyze_sentiment(symbol)
# #     return json.dumps(data)


# # @tool
# # def market_regime_tool() -> str:
# #     """
# #     Analyze overall NIFTY market regime (Bullish/Bearish/Neutral).
# #     """
# #     data = analyze_market_regime()
# #     return json.dumps(data)


# # # List of all tools
# # tools = [
# #     market_tool,
# #     risk_tool,
# #     sentiment_tool,
# #     market_regime_tool,
# # ]


# # # --------------------------------------------------
# # # 🤖 LLM INITIALIZATION (Gemini)
# # # --------------------------------------------------

# # model = ChatGoogleGenerativeAI(
# #     model="gemini-2.5-flash",
# #     google_api_key=GEMINI_API_KEY,
# #     temperature=0.2,
# # )


# # # --------------------------------------------------
# # # 🧠 CREATE AGENT (LangChain v1 Style)
# # # --------------------------------------------------

# # agent = create_agent(
# #     model=model,
# #     tools=tools,
# # )


# # # --------------------------------------------------
# # # 🚀 RUN AGENT
# # # --------------------------------------------------

# # def run_langchain_agent(symbol: str):
# #     """
# #     Executes the LangChain multi-tool agent to analyze a stock
# #     and return structured investment decision.
# #     """

# #     try:
# #         response = agent.invoke(
# #             {
# #                 "messages": [
# #                     {
# #                         "role": "user",
# #                         "content": f"""
# #                         You are a professional financial AI analyst.

# #                         Analyze stock {symbol} using available tools.

# #                         Consider:
# #                         - Technical indicators
# #                         - Risk level
# #                         - News sentiment
# #                         - Overall market regime (NIFTY)

# #                         Combine all factors intelligently.

# #                         Return STRICTLY valid JSON:

# #                         {{
# #                             "action": "BUY/SELL/HOLD",
# #                             "confidence": number (0-100),
# #                             "reasoning": "clear professional explanation"
# #                         }}
# #                         """
# #                     }
# #                 ]
# #             }
# #         )

# #         # Extract last assistant message
# #         final_output = response["messages"][-1].content

# #         # Try parsing JSON cleanly
# #         try:
# #             parsed = json.loads(final_output)
# #             return {
# #                 "langchain_decision": parsed
# #             }
# #         except Exception:
# #             return {
# #                 "langchain_decision_raw": final_output
# #             }

# #     except Exception as e:
# #         return {
# #             "error": "LangChain agent execution failed",
# #             "details": str(e)
# #         }




# import json
# from langchain_core.tools import tool
# from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.agents.market_agent import analyze_market
# from app.agents.risk_agent import analyze_risk
# from app.agents.sentiment_agent import analyze_sentiment
# from app.agents.market_regime_agent import analyze_market_regime
# from app.config import GEMINI_API_KEY


# # ----------------------------
# # Tools
# # ----------------------------

# @tool
# def market_tool(symbol: str, period: str, investment: float):
#     """Fetch stock technical data and portfolio simulation."""
#     return analyze_market(symbol, period, investment)


# @tool
# def risk_tool(symbol: str):
#     """Fetch volatility and risk classification."""
#     return analyze_risk(symbol)


# @tool
# def sentiment_tool(symbol: str):
#     """Fetch news sentiment for stock."""
#     return analyze_sentiment(symbol)


# @tool
# def regime_tool():
#     """Fetch overall market regime."""
#     return analyze_market_regime()


# tools = [market_tool, risk_tool, sentiment_tool, regime_tool]


# # ----------------------------
# # Gemini Model
# # ----------------------------

# model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.2,
# )


# agent = create_agent(
#     model=model,
#     tools=tools,
# )


# # ----------------------------
# # Run Agent
# # ----------------------------

# def run_langchain_agent(symbol: str, period: str, investment: float):

#     response = agent.invoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": f"""
#                     Analyze stock {symbol}.

#                     You MUST use available tools:
#                     - market_tool
#                     - risk_tool
#                     - sentiment_tool
#                     - regime_tool

#                     Based on:
#                     - Technical indicators
#                     - Risk level
#                     - Sentiment
#                     - Market regime
#                     - Portfolio simulation (investment: {investment})

#                     Return STRICT JSON only in this format:

#                     {{
#                         "action": "BUY/SELL/HOLD",
#                         "confidence": 0-100,
#                         "reasoning": "short explanation"
#                     }}
#                     """
#                 }
#             ]
#         }
#     )

#     output_text = response["messages"][-1].content

#     try:
#         parsed = json.loads(output_text)
#     except:
#         return {
#             "error": "Invalid JSON from LLM",
#             "raw_output": output_text
#         }

#     return {
#         "engine": "langchain",
#         "decision": parsed
#     }






import json
import re

from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.market_agent import analyze_market
from app.agents.risk_agent import analyze_risk
from app.agents.sentiment_agent import analyze_sentiment
from app.agents.market_regime_agent import analyze_market_regime
from app.config import GEMINI_API_KEY


# ----------------------------
# Tools
# ----------------------------

@tool
def market_tool(symbol: str):
    """Fetch technical indicators, price history and portfolio simulation."""
    return analyze_market(symbol, "3mo", 100000)


@tool
def risk_tool(symbol: str):
    """Calculate stock volatility and classify risk level."""
    return analyze_risk(symbol)


@tool
def sentiment_tool(symbol: str):
    """Analyze recent news sentiment for a stock."""
    return analyze_sentiment(symbol)


@tool
def regime_tool():
    """Analyze overall NIFTY market regime."""
    return analyze_market_regime()


tools = [market_tool, risk_tool, sentiment_tool, regime_tool]


# ----------------------------
# Model
# ----------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1,
)

agent = create_agent(
    model=model,
    tools=tools,
)


# ----------------------------
# Core Runner
# ----------------------------

def run_langchain_agent(
    symbol: str,
    period: str = "3mo",
    investment: float = 100000,
):
    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
You are a professional AI Investment Decision System.

Analyze stock: {symbol}

You MUST call:
- market_tool
- risk_tool
- sentiment_tool
- regime_tool

Return STRICT JSON only:

{{
  "action": "BUY/SELL/HOLD",
  "confidence": 0-100,
  "reasoning": "short explanation"
}}

Only valid JSON.
"""
                    }
                ]
            }
        )

        # Extract output safely
        last_message = response["messages"][-1]
        raw_content = last_message.content

        # Handle list format (LangChain v1)
        if isinstance(raw_content, list):
            raw_text = ""
            for block in raw_content:
                if isinstance(block, dict) and "text" in block:
                    raw_text += block["text"]
        else:
            raw_text = raw_content

        cleaned = re.sub(r"```json|```", "", raw_text).strip()
        decision_json = json.loads(cleaned)

        # Structured data for frontend
        market_data = analyze_market(symbol, period, investment)
        risk_data = analyze_risk(symbol)
        sentiment_data = analyze_sentiment(symbol)
        market_regime = analyze_market_regime()

        return {
            "engine": "langchain",
            "market_regime": market_regime,
            "market_data": market_data,
            "risk_data": risk_data,
            "sentiment_data": sentiment_data,
            "decision": decision_json,
        }

    except Exception as e:
        return {
            "error": "LangChain execution failed",
            "details": str(e),
        }
