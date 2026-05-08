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

    const interval = setInterval(() => {
      loadScanner();
    }, 15000);

    return () => clearInterval(interval);

  }, []);

  const styles = {

    page: {
      background: "#050505",
      minHeight: "100vh",
      color: "white",
      padding: "20px",
      fontFamily: "Arial"
    },

    table: {
      width: "100%",
      borderCollapse: "collapse",
      marginTop: "20px"
    },

    th: {
      background: "#00ffaa",
      color: "#000",
      padding: "14px",
      fontSize: "18px"
    },

    td: {
      padding: "14px",
      borderBottom: "1px solid #222",
      textAlign: "center"
    }

  };

  return (

    <div style={styles.page}>

      <h1 style={{ fontSize: "52px" }}>
        🚀 CRYPTO SCANNER
      </h1>

      <p style={{ color: "#00ffaa" }}>
        {status}
      </p>

      <table style={styles.table}>

        <thead>

          <tr>
            <th style={styles.th}>Token</th>
            <th style={styles.th}>Price</th>
            <th style={styles.th}>24h %</th>
            <th style={styles.th}>Liquidity</th>
            <th style={styles.th}>Volume</th>
            <th style={styles.th}>Score</th>
            <th style={styles.th}>Rating</th>
          </tr>

        </thead>

        <tbody>

          {coins.map((coin, i) => (

            <tr
              key={i}
              style={{
                background:
                  coin.score >= 80
                    ? "#102010"
                    : "transparent"
              }}
            >

              <td style={styles.td}>
                {coin.name}
              </td>

              <td style={styles.td}>
                $
                {Number(
                  coin.price
                ).toLocaleString()}
              </td>

              <td
                style={{
                  ...styles.td,
                  color:
                    coin.change >= 0
                      ? "#00ff99"
                      : "red",
                  fontWeight: "bold"
                }}
              >
                {coin.change}%
              </td>

              <td style={styles.td}>
                $
                {Number(
                  coin.liquidity
                ).toLocaleString()}
              </td>

              <td style={styles.td}>
                $
                {Number(
                  coin.volume
                ).toLocaleString()}
              </td>

              <td
                style={{
                  ...styles.td,
                  color:
                    coin.score >= 80
                      ? "#00ff99"
                      : "#fff",
                  fontWeight: "bold"
                }}
              >
                {coin.score}
              </td>

              <td style={styles.td}>

                <span
                  style={{
                    background:
                      coin.rating === "🔥 HOT"
                        ? "#ff0033"
                        : coin.rating === "🚀 GOOD"
                        ? "#00aa66"
                        : "#444",

                    padding: "6px 12px",
                    borderRadius: "10px",
                    fontWeight: "bold"
                  }}
                >
                  {coin.rating}
                </span>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}