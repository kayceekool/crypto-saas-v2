import { useEffect, useState } from "react";

export default function Scanner() {
  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading scanner...");

  useEffect(() => {
    async function loadScanner() {
      try {
        setStatus("Connecting to backend...");

        const response = await fetch(
          "https://crypto-saas-v2.onrender.com/scan"
        );

        const data = await response.json();

        console.log(data);

        if (Array.isArray(data)) {
          setCoins(data);
          setStatus("");
        } else {
          setStatus("No tokens received");
        }

      } catch (error) {
        console.log(error);
        setStatus("Backend temporarily waking up...");
      }
    }

    loadScanner();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>🚀 Crypto Scanner</h1>

      {status && (
        <p style={{ color: "red" }}>
          {status}
        </p>
      )}

      <table
        border="1"
        cellPadding="10"
        style={{
          marginTop: 20,
          width: "100%",
          borderCollapse: "collapse"
        }}
      >
        <thead style={{ background: "black", color: "lime" }}>
          <tr>
            <th>Token</th>
            <th>Price ($)</th>
            <th>24h %</th>
          </tr>
        </thead>

        <tbody>
          {coins.map((coin, index) => (
            <tr key={index}>
              <td>{coin.name}</td>

              <td>
                ${coin.price}
              </td>

              <td
                style={{
                  color:
                    coin.change >= 0
                      ? "green"
                      : "red"
                }}
              >
                {coin.change}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}