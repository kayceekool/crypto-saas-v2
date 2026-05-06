import { useEffect, useState } from "react";

export default function Scanner() {
  const [coins, setCoins] = useState([]);
  const [error, setError] = useState("Loading...");

  useEffect(() => {
    const fetchScan = async () => {
      try {
        const res = await fetch("https://crypto-saas-v2.onrender.com/scan");

        if (!res.ok) throw new Error("Server waking up");

        const data = await res.json();

        if (Array.isArray(data) && data.length > 0) {
          setCoins(data);
          setError(null);
        } else {
          setError("No data yet...");
        }

      } catch (err) {
        console.log("Retrying...", err);
        setError("Connecting...");

        setTimeout(fetchScan, 3000); // retry
      }
    };

    fetchScan();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚀 Crypto Scanner</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table style={{ width: "100%", marginTop: "20px" }}>
        <thead style={{ background: "black", color: "lime" }}>
          <tr>
            <th>Token</th>
            <th>Price ($)</th>
            <th>24h %</th>
          </tr>
        </thead>
        <tbody>
          {coins.map((coin, i) => (
            <tr key={i}>
              <td>{coin.name}</td>
              <td>${coin.price}</td>
              <td style={{ color: coin.change > 0 ? "green" : "red" }}>
                {coin.change}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}