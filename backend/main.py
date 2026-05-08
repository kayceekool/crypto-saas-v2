import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading scanner...");

  async function loadScanner() {

    try {

      setStatus("Updating market data...");

      const response = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await response.json();

      console.log("Scanner data:", data);

      if (Array.isArray(data)) {

        setCoins(data);

        setStatus(
          "Live market data • Auto-refresh every 15s"
        );

      } else {

        setStatus("Invalid scanner response");

      }

    } catch (err) {

      console.log(err);

      setStatus("Backend connection failed");

    }
  }

  useEffect(() => {

    // 🔥 first load
    loadScanner();

    // 🔥 auto refresh every 15 seconds
    const interval = setInterval(() => {
      loadScanner();
    }, 15000);

    // cleanup
    return () => clearInterval(interval);

  }, []);

  const page = {
    background: "#050505",
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
    background: "#00ffaa",
    color: "#000",
    padding: "16px",
    fontSize: "22px"
  };

  const td = {
    padding: "18px",
    borderBottom: "1px solid #222",
    textAlign: "center",
    fontSize: "20px"
  };

  return (

    <div style={page}>

      <h1
        style={{
          fontSize: "60px",
          marginBottom: "10px"
        }}
      >
        🚀 Crypto Scanner
      </h1>

      <p
        style={{
          color: "#00ffaa",
          fontSize: "18px"
        }}
      >
        {status}
      </p>

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

              <td style={td}>
                {coin.name}
              </td>

              <td style={td}>
                $
                {Number(
                  coin.price
                ).toLocaleString()}
              </td>

              <td
                style={{
                  ...td,
                  color:
                    coin.change >= 0
                      ? "#00ff99"
                      : "red",
                  fontWeight: "bold"
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