import { useEffect, useState } from "react";

export default function Home() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrices = () => {
      fetch("https://crypto-saas-v2.onrender.com/prices")
        .then(res => res.json())
        .then(data => {
          if (data && data.bitcoin) {
            setPrices(data);     // ✅ update only when valid
            setError(null);
          } else {
            setError("Temporary issue… retrying");
          }
        })
        .catch(() => {
          setError("Connection issue… retrying");
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
    textAlign: "center",
    fontSize: "18px",
    boxShadow: "0 0 10px rgba(0,255,0,0.3)"
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {/* Show error but DO NOT remove prices */}
      {error && <p style={{ color: "orange" }}>{error}</p>}

      {/* Keep last good data */}
      {prices ? (
        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          <div style={card}>
            <strong>BTC</strong>
            <br />
            ${prices.bitcoin?.usd ?? "N/A"}
          </div>

          <div style={card}>
            <strong>ETH</strong>
            <br />
            ${prices.ethereum?.usd ?? "N/A"}
          </div>

          <div style={card}>
            <strong>BNB</strong>
            <br />
            ${prices.binancecoin?.usd ?? "N/A"}
          </div>
        </div>
      ) : (
        <p>Loading prices...</p>
      )}
    </div>
  );
}