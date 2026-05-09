import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState(
    "Loading institutional sniper AI..."
  );

  const [loading, setLoading] = useState(false);

  async function loadScanner() {

    try {

      setLoading(true);

      const res = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await res.json();

      console.log(data);

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
    padding: "14px",
    fontSize: "16px"
  };

  const td = {
    padding: "14px",
    borderBottom: "1px solid #222",
    textAlign: "center",
    fontSize: "14px"
  };

  return (

    <div style={page}>

      <h1
        style={{
          fontSize: "42px",
          marginBottom: "10px"
        }}
      >
        🚀 CRYPTO SCANNER
      </h1>

      <p
        style={{
          color: "#00ffaa",
          fontSize: "18px"
        }}
      >
        {status}
      </p>

      {loading && (

        <p style={{ color: "#888" }}>
          Updating live market data...
        </p>

      )}

      <table style={table}>

        <thead>

          <tr>

            <th style={th}>Type</th>

            <th style={th}>Token</th>

            <th style={th}>Price</th>

            <th style={th}>24h %</th>

            <th style={th}>Liquidity</th>

            <th style={th}>Volume</th>

            <th style={th}>Score</th>

            <th style={th}>Rating</th>

            <th style={th}>Risk</th>

            <th style={th}>Signal</th>

          </tr>

        </thead>

        <tbody>

          {coins.map((coin, i) => (

            <tr key={i}>

              {/* TYPE */}

              <td style={td}>

                <span
                  style={{
                    background:
                      coin.type === "NEW"
                        ? "#ff0080"
                        : "#00ffaa",

                    color:
                      coin.type === "NEW"
                        ? "#fff"
                        : "#000",

                    padding: "5px 10px",

                    borderRadius: "10px",

                    fontWeight: "bold"
                  }}
                >

                  {coin.type}

                </span>

              </td>

              {/* TOKEN */}

              <td style={td}>

                <a
                  href={coin.url}
                  target="_blank"
                  rel="noreferrer"
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

              <td style={td}>

                ${Number(
                  coin.price
                ).toLocaleString()}

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

                {coin.change}%

              </td>

              {/* LIQUIDITY */}

              <td style={td}>

                $
                {Number(
                  coin.liquidity
                ).toLocaleString()}

              </td>

              {/* VOLUME */}

              <td style={td}>

                $
                {Number(
                  coin.volume
                ).toLocaleString()}

              </td>

              {/* SCORE */}

              <td style={td}>

                <b>{coin.score}</b>

              </td>

              {/* RATING */}

              <td style={td}>

                {coin.rating}

              </td>

              {/* RISK */}

              <td
                style={{
                  ...td,

                  color:
                    coin.risk === "LOW"
                      ? "#00ff99"
                      : coin.risk === "MEDIUM"
                      ? "orange"
                      : "red"
                }}
              >

                <b>{coin.risk}</b>

              </td>

              {/* SIGNAL */}

              <td
                style={{
                  ...td,

                  color:
                    coin.signal === "STRONG BUY"
                      ? "#00ff99"
                      : coin.signal === "BUY"
                      ? "#00ffaa"
                      : "#777",

                  fontWeight: "bold"
                }}
              >

                {coin.signal}

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );
}