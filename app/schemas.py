from pydantic import BaseModel

# Request model
class StockRequest(BaseModel):
    symbol: str


# Market Agent Output
class MarketResponse(BaseModel):
    symbol: str
    current_price: float
    sma_20: float
    rsi_14: float


# Risk Agent Output
class RiskResponse(BaseModel):
    volatility: float
    risk_level: str


# Final Decision Output
class DecisionResponse(BaseModel):
    action: str
    confidence: float
    reasoning: str
