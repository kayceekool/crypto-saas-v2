import { useEffect, useState } from "react";

export default function Home() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com/prices")
      .then(res => res.json())
      .then(data => {
        if (!data || data.error) {
          setError("Failed to load prices");
        } else {
          setPrices(data);
        }
      })
      .catch(() => setError("Backend connection failed"));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {/* Loading */}
      {!prices && !error && <p>Loading prices...</p>}

      {/* Error */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Data */}
      {prices && prices.bitcoin && (
        <div>
          <p>BTC: ${prices.bitcoin?.usd ?? "N/A"}</p>
          <p>ETH: ${prices.ethereum?.usd ?? "N/A"}</p>
          <p>BNB: ${prices.binancecoin?.usd ?? "N/A"}</p>
        </div>
      )}
    </div>
  );
}