def make_decision(market_data, risk_data, sentiment_data, market_regime):
    price = market_data["current_price"]
    sma = market_data["sma_20"]
    rsi = market_data["rsi_14"]

    risk_level = risk_data["risk_level"]
    sentiment_score = sentiment_data.get("score", 0)
    regime = market_regime.get("regime", "Neutral")

    score = 0

    # ------------------------
    # 1️⃣ Trend Component (Weight 2)
    # ------------------------
    if price > sma:
        score += 2
    else:
        score -= 2

    # ------------------------
    # 2️⃣ Momentum (RSI) (Weight 1)
    # ------------------------
    if rsi < 30:
        score += 1
    elif rsi > 70:
        score -= 1

    # ------------------------
    # 3️⃣ Risk Adjustment (Weight 1)
    # ------------------------
    if risk_level == "Low":
        score += 1
    elif risk_level == "High":
        score -= 1

    # ------------------------
    # 4️⃣ Sentiment Component (Weight 2 scaled)
    # ------------------------
    score += sentiment_score * 2

    # ------------------------
    # 5️⃣ Market Regime Filter
    # ------------------------
    if regime == "Bearish":
        score -= 2
    elif regime == "Bullish":
        score += 1

    # ------------------------
    # Final Decision Logic
    # ------------------------
    if score >= 3:
        action = "BUY"
    elif score <= -3:
        action = "SELL"
    else:
        action = "HOLD"

    confidence = min(abs(score) * 15, 100)

    reasoning = (
        f"Composite Score: {round(score,2)} | "
        f"Trend + Momentum + Risk + Sentiment + Market Regime considered."
    )

    return {
        "action": action,
        "confidence": round(confidence, 2),
        "reasoning": reasoning
    }
