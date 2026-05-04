import { useEffect, useState } from "react";

export default function Home() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com/prices")
      .then(res => res.json())
      .then(data => {
        if (!data || data.error) {
          setError("Invalid data from backend");
        } else {
          setPrices(data);
        }
      })
      .catch(() => setError("Failed to fetch prices"));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {!prices && !error && <p>Loading prices...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

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