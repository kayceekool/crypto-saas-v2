import { useEffect, useState } from "react";

export default function Home() {
  const [coins, setCoins] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScan = () => {
      fetch("https://crypto-saas-v2.onrender.com/scan")
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setCoins(data);
            setError(null);
          } else {
            setError("Scan failed");
          }
        })
        .catch(() => setError("Connection error"));
    };

    fetchScan();
    const interval = setInterval(fetchScan, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🚀 Crypto Scanner</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table style={{ width: "100%", marginTop: "20px", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#111", color: "#0f0" }}>
            <th style={cell}>Token</th>
            <th style={cell}>Price ($)</th>
            <th style={cell}>24h %</th>
          </tr>
        </thead>
        <tbody>
          {coins.map((coin, i) => (
            <tr key={i} style={{ textAlign: "center" }}>
              <td style={cell}>{coin.name}</td>
              <td style={cell}>${coin.price}</td>
              <td style={{
                ...cell,
                color: coin.change > 0 ? "lime" : "red"
              }}>
                {coin.change}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const cell = {
  padding: "10px",
  borderBottom: "1px solid #333"
};