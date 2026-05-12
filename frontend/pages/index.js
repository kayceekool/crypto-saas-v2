import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading AI sniper...");
  const [loading, setLoading] = useState(false);

  async function loadScanner() {

    try {

      setLoading(true);

      const res = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await res.json();

      if (data.scanner) {

        setCoins(data.scanner);

        setStatus(
          `🔥 Live Sniper AI • ${data.scanner.length} tokens`
        );

      } else {

        setStatus("Invalid backend response");

      }

    } catch (err) {

      console.log(err);

      setStatus("Backend connection failed");

    } finally {

      setLoading(false);

    }
  }

  useEffect(() => {

    loadScanner();

    const interval = setInterval(
      loadScanner,
      15000
    );

    return () => clearInterval(interval);

  }, []);

  return (

    <div
      style={{
        padding: 20,
        background: "#050505",
        color: "#fff",
        minHeight: "100vh",
        fontFamily: "Arial"
      }}
    >

      <h1>
        🚀 CRYPTO SCANNER
      </h1>

      <p
        style={{
          color: "#00ffaa",
          fontWeight: "bold"
        }}
      >
        {status}
      </p>

      <p
        style={{
          color: "#888"
        }}
      >
        ⚡ AI engine online
      </p>

      {loading && (

        <p
          style={{
            color: "#ffaa00"
          }}
        >
          Updating live market data...
        </p>

      )}

      <div
        style={{
          overflowX: "auto"
        }}
      >

        <table
          style={{
            width: "100%",
            marginTop: 20,
            borderCollapse: "collapse"
          }}
        >

          <thead>

            <tr
              style={{
                background: "#111"
              }}
            >

              <th>Type</th>
              <th>Token</th>
              <th>Price</th>
              <th>24h %</th>
              <th>Liquidity</th>
              <th>Volume</th>
              <th>Score</th>
              <th>Rating</th>
              <th>Risk</th>
              <th>Signal</th>
              <th>Confidence</th>
              <th>Whales</th>
              <th>Age</th>

            </tr>

          </thead>

          <tbody>

            {coins.map((coin, i) => (

              <tr
                key={i}
                style={{
                  borderBottom: "1px solid #222"
                }}
              >

                <td>{coin.type}</td>

                <td>

                  <a
                    href={coin.url}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      color: "#00ccff",
                      textDecoration: "none",
                      fontWeight: "bold"
                    }}
                  >
                    {coin.name}
                  </a>

                </td>

                <td>

                  {coin.price > 0

                    ? `$${Number(
                        coin.price
                      ).toLocaleString()}`

                    : "$0"}

                </td>

                <td
                  style={{
                    color:
                      coin.change >= 0
                        ? "#00ff99"
                        : "red"
                  }}
                >
                  {coin.change}%
                </td>

                <td>
                  $
                  {Number(
                    coin.liquidity
                  ).toLocaleString()}
                </td>

                <td>
                  $
                  {Number(
                    coin.volume
                  ).toLocaleString()}
                </td>

                <td>
                  <b>{coin.score}</b>
                </td>

                <td>{coin.rating}</td>

                <td>
                  <b>{coin.risk}</b>
                </td>

                <td>{coin.signal}</td>

                <td>

                  <span
                    style={{
                      color:
                        coin.confidence >= 85
                          ? "#00ff99"
                          : coin.confidence >= 70
                          ? "#ffaa00"
                          : "#888"
                    }}
                  >
                    {coin.confidence}%
                  </span>

                </td>

                <td>

                  {coin.whale_signal}

                </td>

                <td>

                  {coin.age_minutes < 60

                    ? `${coin.age_minutes}m`

                    : `${(
                        coin.age_minutes / 60
                      ).toFixed(1)}h`
                  }

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}