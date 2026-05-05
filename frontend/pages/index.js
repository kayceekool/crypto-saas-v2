import { useEffect, useState } from "react";

export default function Home() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrices = () => {
      fetch("https://crypto-saas-v2.onrender.com/prices")
        .then(res => res.json())
        .then(data => {
          if (!data || data.error) {
            setError("Failed to load prices");
          } else {
            setPrices(data);
            setError(null);
          }
        })
        .catch(() => setError("Backend connection failed"));
    };

    fetchPrices(); // initial load

    const interval = setInterval(fetchPrices, 10000); // refresh every 10s

    return () => clearInterval(interval);
  }, []);

  const card = {
    padding: "20px",
    borderRadius: "10px",
    background: "#111",
    color: "#0f0",
    minWidth: "120px",
    textAlign: "center",
    fontSize: "18px",
    boxShadow: "0 0 10px rgba(0,255,0,0.3)"
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {/* Loading */}
      {!prices && !error && <p>Loading prices...</p>}

      {/* Error */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Prices */}
      {prices && prices.bitcoin && (
        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          <div style={card}>
            <strong>BTC</strong>
            <br />
            ${prices.bitcoin.usd}
          </div>

          <div style={card}>
            <strong>ETH</strong>
            <br />
            ${prices.ethereum.usd}
          </div>

          <div style={card}>
            <strong>BNB</strong>
            <br />
            ${prices.binancecoin.usd}
          </div>
        </div>
      )}
    </div>
  );
}