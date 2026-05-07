import { useEffect, useState } from "react";

export default function Scanner() {
  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading scanner...");

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com/scanner")
      .then((res) => res.json())
      .then((data) => {
        console.log("Scanner API:", data);

        if (Array.isArray(data)) {
          setCoins(data);
          setStatus("");
        } else {
          setStatus("Invalid scanner response");
        }
      })
      .catch((err) => {
        console.log(err);
        setStatus("Connection error");
      });
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
    <div
      style={{
        background: "#f4f4f4",
        minHeight: "100vh",
        padding: "20px",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ fontSize: "56px", marginBottom: "20px" }}>
        🚀 Crypto Scanner
      </h1>

      {status && (
        <p style={{ color: "red", fontSize: "24px" }}>{status}</p>
      )}

      {coins.length === 0 && (
        <p style={{ fontSize: "22px" }}>Loading scanner data...</p>
      )}

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