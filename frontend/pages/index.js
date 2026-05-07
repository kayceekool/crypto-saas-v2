import { useEffect, useState } from "react";

export default function Home() {
  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading scanner data...");

  useEffect(() => {
    async function loadScanner() {
      try {
        const response = await fetch(
          "https://crypto-saas-v2.onrender.com/scan"
        );

        const data = await response.json();

        console.log("SCAN DATA:", data);

        if (Array.isArray(data) && data.length > 0) {
          setCoins(data);
          setStatus("");
        } else {
          setStatus("No scanner data received");
        }

      } catch (error) {
        console.log(error);
        setStatus("Backend connection failed");
      }
    }

    loadScanner();
  }, []);

  const page = {
    background: "#111",
    minHeight: "100vh",
    color: "white",
    padding: "20px",
    fontFamily: "Arial"
  };

  const table = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "20px"
  };

  const th = {
    background: "#00ff99",
    color: "#000",
    padding: "14px",
    fontSize: "18px"
  };

  const td = {
    padding: "12px",
    borderBottom: "1px solid #333",
    textAlign: "center"
  };

  return (
    <div style={page}>
      <h1>🚀 Crypto Scanner</h1>

      {status && (
        <p style={{ color: "orange" }}>
          {status}
        </p>
      )}

      {coins.length > 0 && (
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

                <td style={td}>
                  ${coin.price}
                </td>

                <td
                  style={{
                    ...td,
                    color:
                      coin.change >= 0
                        ? "#00ff99"
                        : "red"
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