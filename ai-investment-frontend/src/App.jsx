// import { useState } from "react";
// import "./App.css";

// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   Tooltip,
//   ResponsiveContainer,
//   CartesianGrid,
// } from "recharts";

// function App() {
//   const [symbol, setSymbol] = useState("");
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const quickStocks = [
//     "INFY.NS",
//     "RELIANCE.NS",
//     "HDFCBANK.NS",
//     "TCS.NS",
//     "ICICIBANK.NS",
//   ];

//   const handleAnalyzeStock = async (stockSymbol) => {
//     setLoading(true);
//     setError(null);
//     setData(null);

//     try {
//       const response = await fetch(
//         `http://127.0.0.1:8000/analyze/${stockSymbol}`
//       );
// //       const response = await fetch(
// //   `http://127.0.0.1:8000/langchain/${stockSymbol}`
// // );


//       const result = await response.json();

//       if (!response.ok || result.error) {
//         throw new Error(result.error || "Backend error");
//       }

//       setData(result);
//     } catch (err) {
//       setError(err.message || "Backend not running");
//     }

//     setLoading(false);
//   };

//   const handleAnalyze = () => {
//     if (!symbol) return;

//     let formattedSymbol = symbol.toUpperCase();

//     if (!formattedSymbol.includes(".")) {
//       formattedSymbol += ".NS";
//     }

//     handleAnalyzeStock(formattedSymbol);
//   };

//   const handleQuickSelect = (stock) => {
//     setSymbol(stock);
//     handleAnalyzeStock(stock);
//   };

//   const getActionColor = (action) => {
//     if (action === "BUY") return "#22c55e";
//     if (action === "SELL") return "#ef4444";
//     return "#9ca3af";
//   };

//   return (
//     <div className={`container ${!data ? "centered" : ""}`}>
//       <h1 className="title">
//         AI Market-Aware Investment Decision System
//       </h1>

//       {/* Input */}
//       <div className="input-section">
//         <input
//           type="text"
//           placeholder="Enter stock symbol (e.g., INFY or INFY.NS)"
//           value={symbol}
//           onChange={(e) => setSymbol(e.target.value)}
//           className="input"
//         />
//         <button onClick={handleAnalyze} className="button">
//           Analyze
//         </button>
//       </div>

//       {/* Quick Stocks */}
//       <div className="quick-stocks">
//         {quickStocks.map((stock, index) => (
//           <button
//             key={index}
//             className="quick-stock-btn"
//             onClick={() => handleQuickSelect(stock)}
//           >
//             {stock}
//           </button>
//         ))}
//       </div>

//       {loading && <p className="status">Analyzing market data...</p>}
//       {error && <p className="error">{error}</p>}

//       {/* SAFE RENDER */}
//       {data && !data.error && (
//         <div className="dashboard">

//           {/* Top Row */}
//           <div className="top-row">

//             {/* Market Regime */}
//             {data.market_regime && (
//               <div className="card">
//                 <h3>📊 Market Regime (NIFTY)</h3>
//                 <p>NIFTY: {data.market_regime?.nifty_price}</p>
//                 <p>SMA 50: {data.market_regime?.sma_50}</p>
//                 <p>RSI: {data.market_regime?.rsi_14}</p>
//                 <p>
//                   <strong>Regime: {data.market_regime?.regime}</strong>
//                 </p>
//               </div>
//             )}

//             {/* Technical */}
//             {data.market_data && (
//               <div className="card">
//                 <h3>📈 Technical Analysis</h3>
//                 <p>Current Price: {data.market_data?.current_price}</p>
//                 <p>SMA 20: {data.market_data?.sma_20}</p>
//                 <p>RSI: {data.market_data?.rsi_14}</p>
//               </div>
//             )}

//             {/* Risk */}
//             {data.risk_data && (
//               <div className="card">
//                 <h3>⚠ Risk Analysis</h3>
//                 <p>Volatility: {data.risk_data?.volatility}</p>
//                 <p>
//                   Risk Level: <strong>{data.risk_data?.risk_level}</strong>
//                 </p>
//               </div>
//             )}

//           </div>

//           {/* Chart */}
//           {data.market_data?.price_history && (
//             <div className="card full-width">
//               <h3>📈 Price Chart (Last 3 Months)</h3>

//               <ResponsiveContainer width="100%" height={320}>
//                 <LineChart data={data.market_data.price_history}>
//                   <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
//                   <XAxis dataKey="date" hide />
//                   <YAxis domain={["auto", "auto"]} />
//                   <Tooltip />
//                   <Line
//                     type="monotone"
//                     dataKey="close"
//                     stroke="#3b82f6"
//                     dot={false}
//                     strokeWidth={2}
//                   />
//                   <Line
//                     type="monotone"
//                     dataKey="sma_20"
//                     stroke="#22c55e"
//                     dot={false}
//                     strokeWidth={2}
//                   />
//                 </LineChart>
//               </ResponsiveContainer>
//             </div>
//           )}

//           {/* Portfolio */}
//           {data.market_data?.portfolio && (
//             <div className="card full-width portfolio-card">
//               <h3>💼 Portfolio Simulation (₹1,00,000 Investment)</h3>

//               <p>
//                 Shares Purchased:{" "}
//                 <strong>{data.market_data.portfolio?.shares}</strong>
//               </p>

//               <p>
//                 Buy Price: ₹
//                 {data.market_data.portfolio?.buy_price_3m_ago}
//               </p>

//               <p>
//                 Current Value: ₹
//                 {data.market_data.portfolio?.current_value}
//               </p>

//               <p
//                 style={{
//                   color:
//                     data.market_data.portfolio?.profit_loss >= 0
//                       ? "#22c55e"
//                       : "#ef4444",
//                   fontWeight: "600",
//                 }}
//               >
//                 P/L: ₹{data.market_data.portfolio?.profit_loss} (
//                 {data.market_data.portfolio?.profit_loss_percent}%)
//               </p>
//             </div>
//           )}

//           {/* Sentiment */}
//           {data.sentiment_data && (
//             <div className="card full-width">
//               <h3>🤖 AI Sentiment</h3>
//               <p>
//                 Sentiment:{" "}
//                 <strong>{data.sentiment_data?.sentiment}</strong>
//               </p>
//               <p>Score: {data.sentiment_data?.score}</p>
//               <p className="reasoning">
//                 {data.sentiment_data?.reason}
//               </p>
//             </div>
//           )}

//           {/* Decision */}
//           {data.decision && (
//             <div className="card final-card">
//               <h2>🎯 Final Decision</h2>

//               <div
//                 className="final-action"
//                 style={{ color: getActionColor(data.decision?.action) }}
//               >
//                 {data.decision?.action}
//               </div>

//               <div className="confidence">
//                 Confidence: {data.decision?.confidence}%
//               </div>

//               <div className="progress-bar">
//                 <div
//                   className="progress-fill"
//                   style={{
//                     width: `${data.decision?.confidence}%`,
//                     backgroundColor: getActionColor(data.decision?.action),
//                   }}
//                 />
//               </div>

//               <div className="reasoning">
//                 {data.decision?.reasoning}
//               </div>
//             </div>
//           )}

//         </div>
//       )}
//     </div>
//   );
// }

// export default App;


import { useState } from "react";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function App() {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const quickStocks = [
    "INFY.NS",
    "RELIANCE.NS",
    "HDFCBANK.NS",
    "TCS.NS",
    "ICICIBANK.NS",
  ];

  const handleAnalyzeStock = async (stockSymbol) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/analyze/${stockSymbol}`
      );

      const result = await response.json();

      if (!response.ok || result.error) {
        throw new Error(result.error || "Backend error");
      }

      setData(result);
    } catch (err) {
      setError(err.message || "Backend not running");
    }

    setLoading(false);
  };

  const handleAnalyze = () => {
    if (!symbol) return;

    let formattedSymbol = symbol.toUpperCase();

    if (!formattedSymbol.includes(".")) {
      formattedSymbol += ".NS";
    }

    handleAnalyzeStock(formattedSymbol);
  };

  const handleQuickSelect = (stock) => {
    setSymbol(stock);
    handleAnalyzeStock(stock);
  };

  const getActionColor = (action) => {
    if (action === "BUY") return "#22c55e";
    if (action === "SELL") return "#ef4444";
    return "#9ca3af";
  };

  return (
    <div className={`container ${!data ? "centered" : ""}`}>
      <h1 className="title">
        AI Market-Aware Investment Decision System
      </h1>

      {/* Input */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter stock symbol (e.g., INFY or INFY.NS)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="input"
        />
        <button onClick={handleAnalyze} className="button">
          Analyze
        </button>
      </div>

      {/* Quick Stocks */}
      <div className="quick-stocks">
        {quickStocks.map((stock, index) => (
          <button
            key={index}
            className="quick-stock-btn"
            onClick={() => handleQuickSelect(stock)}
          >
            {stock}
          </button>
        ))}
      </div>

      {loading && <p className="status">Analyzing market data...</p>}
      {error && <p className="error">{error}</p>}

      {data && !data.error && (
        <div className="dashboard">

          {/* Top Row */}
          <div className="top-row">

            {data.market_regime && (
              <div className="card">
                <h3>📊 Market Regime (NIFTY)</h3>
                <p>NIFTY: {data.market_regime.nifty_price}</p>
                <p>SMA 50: {data.market_regime.sma_50}</p>
                <p>RSI: {data.market_regime.rsi_14}</p>
                <p><strong>Regime: {data.market_regime.regime}</strong></p>
              </div>
            )}

            {data.market_data && (
              <div className="card">
                <h3>📈 Technical Analysis</h3>
                <p>Current Price: {data.market_data.current_price}</p>
                <p>SMA 20: {data.market_data.sma_20}</p>
                <p>RSI: {data.market_data.rsi_14}</p>
              </div>
            )}

            {data.risk_data && (
              <div className="card">
                <h3>⚠ Risk Analysis</h3>
                <p>Volatility: {data.risk_data.volatility}</p>
                <p>
                  Risk Level: <strong>{data.risk_data.risk_level}</strong>
                </p>
              </div>
            )}
          </div>

          {/* Chart */}
          {data.market_data?.price_history && (
            <div className="card full-width">
              <h3>📈 Price Chart (Last 3 Months)</h3>

              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={data.market_data.price_history}>
                  <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                  <XAxis dataKey="date" hide />
                  <YAxis domain={["auto", "auto"]} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="close"
                    stroke="#3b82f6"
                    dot={false}
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="sma_20"
                    stroke="#22c55e"
                    dot={false}
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Portfolio Simulation */}
          {data.market_data?.simulation && (
            <div className="card full-width portfolio-card">
              <h3>💼 Portfolio Simulation (₹1,00,000 Investment)</h3>

              <p>
                Shares Purchased:{" "}
                <strong>{data.market_data.simulation.shares}</strong>
              </p>

              <p>
                Buy Price: ₹{data.market_data.simulation.buy_price}
              </p>

              <p>
                Current Value: ₹{data.market_data.simulation.current_value}
              </p>

              <p
                style={{
                  color:
                    data.market_data.simulation.profit_loss >= 0
                      ? "#22c55e"
                      : "#ef4444",
                  fontWeight: "600",
                }}
              >
                P/L: ₹{data.market_data.simulation.profit_loss} (
                {data.market_data.simulation.return_percent}%)
              </p>
            </div>
          )}

          {/* Sentiment */}
          {data.sentiment_data && (
            <div className="card full-width">
              <h3>🤖 AI Sentiment</h3>
              <p>
                Sentiment: <strong>{data.sentiment_data.sentiment}</strong>
              </p>
              <p>Score: {data.sentiment_data.score}</p>
              <p className="reasoning">
                {data.sentiment_data.reason}
              </p>
            </div>
          )}

          {/* Decision */}
          {data.decision && (
            <div className="card final-card">
              <h2>🎯 Final Decision</h2>

              <div
                className="final-action"
                style={{ color: getActionColor(data.decision.action) }}
              >
                {data.decision.action}
              </div>

              <div className="confidence">
                Confidence: {data.decision.confidence}%
              </div>

              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${data.decision.confidence}%`,
                    backgroundColor: getActionColor(data.decision.action),
                  }}
                />
              </div>

              <div className="reasoning">
                {data.decision.reasoning}
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default App;
