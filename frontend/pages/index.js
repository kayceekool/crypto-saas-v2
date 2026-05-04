import { useEffect, useState } from "react";

export default function Home() {
  const [prices, setPrices] = useState(null);

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com/prices")
      .then(res => res.json())
      .then(data => setPrices(data))
      .catch(() => setPrices("error"));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚀 Crypto Dashboard</h1>

      {!prices && <p>Loading prices...</p>}

      {prices && prices !== "error" && (
        <div>
          <p>BTC: ${prices.bitcoin.usd}</p>
          <p>ETH: ${prices.ethereum.usd}</p>
          <p>BNB: ${prices.binancecoin.usd}</p>
        </div>
      )}

      {prices === "error" && <p>Failed to load prices</p>}
    </div>
  );
}