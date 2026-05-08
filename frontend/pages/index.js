import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState(
    "Loading sniper scanner..."
  );

  async function loadScanner() {

    try {

      const response = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await response.json();

      console.log(data);

      if (Array.isArray(data)) {

        setCoins(data);

        setStatus(
          `🔥 Live Solana Scanner • ${data.length} tokens`
        );

      } else {

        setStatus("Invalid backend response");

      }

    } catch (err) {

      console.log(err);

      setStatus("Backend connection failed");

    }
  }

  useEffect(() => {

    loadScanner();

    // 🔥 auto refresh
    const interval = setInterval(() => {
      loadScanner();
    }, 15000);

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
    fontSize: "18px"
  };

  return (

    <div style={page}>

      <h1
        style={{
          fontSize: "56px",
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
            <th style={th}>Type</th>
            <th style={th}>Token</th>
            <th style={th}>Price ($)</th>
            <th style={th}>24h %</th>
          </tr>

        </thead>

        <tbody>

          {coins.map((coin, i) => (

            <tr key={i}>

              {/* 🔥 TOKEN TYPE */}
              <td style={td}>

                {coin.type === "NEW" ? (

                  <span
                    style={{
                      background: "#ff0080",
                      padding: "6px 12px",
                      borderRadius: "12px",
                      fontWeight: "bold",
                      color: "white"
                    }}
                  >
                    NEW
                  </span>

                ) : (

                  <span
                    style={{
                      background: "#00ffaa",
                      padding: "6px 12px",
                      borderRadius: "12px",
                      fontWeight: "bold",
                      color: "#000"
                    }}
                  >
                    TRENDING
                  </span>

                )}

              </td>

              {/* TOKEN */}
              <td style={td}>
                {coin.name}
              </td>

              {/* PRICE */}
              <td style={td}>

                {coin.price > 0
                  ? `$${Number(
                      coin.price
                    ).toLocaleString()}`
                  : "NEW"}

              </td>

              {/* CHANGE */}
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

                {coin.type === "NEW"
                  ? "JUST LAUNCHED 🚀"
                  : `${coin.change}%`}

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}