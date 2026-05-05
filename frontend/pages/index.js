import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

export default function Home() {
  const [prices, setPrices] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchPrices = () => {
      fetch("https://crypto-saas-v2.onrender.com/prices")
        .then(res => res.json())
        .then(data => {
          if (data && data.bitcoin) {
            setPrices(data);

            // Add to chart history
            setHistory(prev => [
              ...prev.slice(-20), // keep last 20 points
              {
                time: new Date().toLocaleTimeString(),
                btc: data.bitcoin.usd
              }
            ]);
          }
        });
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 10000);

    return () => clearInterval(interval);
  }, []);

  const card = {
    padding: "20px",
    borderRadius: "10px",
    background: "#111",
    color: "#0f0",
    minWidth: "120px",
    textAlign: "center"
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {prices && (
        <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
          <div style={card}>BTC<br/>${prices.bitcoin.usd}</div>
          <div style={card}>ETH<br/>${prices.ethereum.usd}</div>
          <div style={card}>BNB<br/>${prices.binancecoin.usd}</div>
        </div>
      )}

      <h3>📈 BTC Live Chart</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={history}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="btc" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}