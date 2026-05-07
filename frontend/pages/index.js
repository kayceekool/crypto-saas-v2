import { useEffect, useState } from "react";

export default function Home() {
  const [coins, setCoins] = useState([]);

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com/scan")
      .then((res) => res.json())
      .then((data) => {
        setCoins(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const page = {
    background: "#111",
    minHeight: "100vh",
    padding: "20px",
    color: "white",
    fontFamily: "Arial",
  };

  const table = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "20px",
  };

  const th = {
    background: "#00ff99",
    color: "black",
    padding: "12px",
    fontSize: "18px",
  };

  const td = {
    padding: "10px",
    borderBottom: "1px solid #333",
    textAlign: "center",
  };

  return (
    <div style={page}>
      <h1>🚀 Crypto Scanner</h1>

      {coins.length === 0 ? (
        <p>Loading scanner data...</p>
      ) : (
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Token</th>
              <th style={th}>Price ($)</th>
              <th style={th}>24h %</th>
            </tr>
          </thead>

          <tbody>
            {coins.map((coin, i) => (
              <tr key={i}>
                <td style={td}>{coin.name}</td>
                <td style={td}>${coin.price}</td>
                <td
                  style={{
                    ...td,
                    color: coin.change > 0 ? "#00ff99" : "red",
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