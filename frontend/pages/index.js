import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);

  const [status, setStatus] = useState(
    "Loading sniper scanner..."
  );

  // =====================================
  // LOAD SCANNER
  // =====================================

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

  // =====================================
  // AUTO REFRESH
  // =====================================

  useEffect(() => {

    loadScanner();

    const interval = setInterval(() => {

      loadScanner();

    }, 15000);

    return () => clearInterval(interval);

  }, []);

  // =====================================
  // STYLES
  // =====================================

  const styles = {

    page: {

      background: "#050505",

      minHeight: "100vh",

      color: "white",

      padding: "20px",

      fontFamily: "Arial"
    },

    title: {

      fontSize: "56px",

      marginBottom: "10px"
    },

    status: {

      color: "#00ffaa",

      marginBottom: "20px",

      fontSize: "18px"
    },

    table: {

      width: "100%",

      borderCollapse: "collapse",

      marginTop: "20px"
    },

    th: {

      background: "#00ffaa",

      color: "#000",

      padding: "16px",

      fontSize: "18px",

      position: "sticky",

      top: 0
    },

    td: {

      padding: "16px",

      borderBottom: "1px solid #222",

      textAlign: "center",

      fontSize: "16px"
    }

  };

  return (

    <div style={styles.page}>

      <h1 style={styles.title}>
        🚀 CRYPTO SCANNER
      </h1>

      <p style={styles.status}>
        {status}
      </p>

      <table style={styles.table}>

        <thead>

          <tr>

            <th style={styles.th}>Type</th>
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

                  coin.score >= 140

                    ? "#2a0000"

                    : coin.score >= 110

                    ? "#102010"

                    : "transparent",

                boxShadow:

                  coin.score >= 140

                    ? "0 0 20px #ff0000"

                    : "none"
              }}
            >

              {/* TYPE */}

              <td style={styles.td}>

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

              <td style={styles.td}>

                <a

                  href={coin.url}

                  target="_blank"

                  rel="noopener noreferrer"

                  style={{
                    color: "#00ffaa",
                    textDecoration: "none",
                    fontWeight: "bold"
                  }}
                >

                  {coin.name}

                </a>

              </td>

              {/* PRICE */}

              <td style={styles.td}>

                {coin.price > 0.001

                  ? `$${Number(
                      coin.price
                    ).toLocaleString()}`

                  : `$${coin.price.toFixed(8)}`}

              </td>

              {/* CHANGE */}

              <td

                style={{

                  ...styles.td,

                  color:

                    coin.change >= 0

                      ? "#00ff99"

                      : "#ff4444",

                  fontWeight: "bold"
                }}
              >

                {coin.change}%

              </td>

              {/* LIQUIDITY */}

              <td style={styles.td}>

                $

                {Number(
                  coin.liquidity
                ).toLocaleString()}

              </td>

              {/* VOLUME */}

              <td style={styles.td}>

                $

                {Number(
                  coin.volume
                ).toLocaleString()}

              </td>

              {/* SCORE */}

              <td

                style={{

                  ...styles.td,

                  color:

                    coin.score >= 140

                      ? "#ff3333"

                      : coin.score >= 110

                      ? "#00ff99"

                      : "#ffffff",

                  fontWeight: "bold",

                  fontSize: "18px"
                }}
              >

                {coin.score}

              </td>

              {/* RATING */}

              <td style={styles.td}>

                <span

                  style={{

                    background:

                      coin.rating === "🚨 EXTREME"

                        ? "#ff0000"

                        : coin.rating === "🔥 HOT"

                        ? "#ff6600"

                        : coin.rating === "🚀 GOOD"

                        ? "#00aa66"

                        : coin.rating === "👀 WATCH"

                        ? "#666600"

                        : "#444",

                    padding: "6px 12px",

                    borderRadius: "10px",

                    fontWeight: "bold",

                    color: "white"
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