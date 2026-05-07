import { useEffect, useState } from "react";

export default function Scanner() {
  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading scanner...");

  useEffect(() => {
    async function loadScanner() {
      try {
        const res = await fetch(
          "https://crypto-saas-v2.onrender.com/scan"
        );

        if (!res.ok) {
          throw new Error("Backend not ready");
        }

        const text = await res.text();
        console.log("Scanner RAW:", text);

        let data = JSON.parse(text);

        if (Array.isArray(data)) {
          setCoins(data);
          setStatus("");
        } else {
          setStatus("Invalid scanner response");
        }

      } catch (err) {
        console.log(err);
        setStatus("Connection error / backend waking up");
      }
    }

    loadScanner();
  }, []);

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "20px",
  };

  const headStyle = {
    background: "#000",
    color: "#39ff14",
    fontSize: "22px",
  };

  const cellStyle = {
    padding: "14px",
    borderBottom: "1px solid #333",
    textAlign: "center",
    fontSize: "18px",
  };

  return (
    <div style={{ background: "#f4f4f4", minHeight: "100vh", padding: "20px" }}>
      <h1>🚀 Crypto Scanner</h1>

      {status && <p style={{ color: "red" }}>{status}</p>}

      {coins.length === 0 && <p>Waiting for data...</p>}

      {coins.length > 0 && (
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headStyle}>Token</th>
              <th style={headStyle}>Price ($)</th>
              <th style={headStyle}>24h %</th>
            </tr>
          </thead>

          <tbody>
            {coins.map((coin, i) => (
              <tr key={i}>
                <td style={cellStyle}>{coin.name}</td>
                <td style={cellStyle}>
                  ${Number(coin.price).toLocaleString()}
                </td>
                <td
                  style={{
                    ...cellStyle,
                    color: coin.change >= 0 ? "limegreen" : "red",
                    fontWeight: "bold",
                  }}
                >
                  {coin.change}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}