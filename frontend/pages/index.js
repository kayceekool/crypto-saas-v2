import { useEffect, useState } from "react";

export default function Home() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState(
    "Loading sniper engine..."
  );

  const [loading, setLoading] = useState(false);

  async function loadScanner() {

    try {

      setLoading(true);

      const res = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await res.json();

      const scannerData = data.scanner || [];

      setCoins(scannerData);

      setStatus(
        `🔥 Live Sniper AI • ${scannerData.length} tokens`
      );

      setLoading(false);

    } catch (err) {

      console.log(err);

      setStatus("Backend connection failed");

      setLoading(false);
    }
  }

  useEffect(() => {

    loadScanner();

    const interval = setInterval(
      loadScanner,
      30000
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
        overflowX: "auto"
      }}
    >

      <h1>
        🚀 CRYPTO SCANNER
      </h1>

      <p style={{ color: "#00ffaa" }}>
        {status}
      </p>

      <p style={{ color: "#999" }}>
        ⚡ AI engine online
      </p>

      {loading && (

        <p style={{ color: "#666" }}>
          Syncing live market data...
        </p>

      )}

      <table
        style={{
          width: "100%",
          marginTop: 20,
          borderCollapse: "collapse"
        }}
      >

        <thead>

          <tr>

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

            <tr key={i}>

              <td>
                {coin.type}
              </td>

              <td>

                <a
                  href={coin.url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    color: "#00ffaa",
                    textDecoration: "none"
                  }}
                >
                  {coin.name}
                </a>

              </td>

              <td>
                $
                {Number(
                  coin.price || 0
                ).toLocaleString()}
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
                  coin.liquidity || 0
                ).toLocaleString()}
              </td>

              <td>
                $
                {Number(
                  coin.volume || 0
                ).toLocaleString()}
              </td>

              <td>
                <b>{coin.score}</b>
              </td>

              <td>
                {coin.rating}
              </td>

              <td>
                <b>{coin.risk}</b>
              </td>

              <td>
                {coin.signal}
              </td>

              <td>
                {coin.confidence}
              </td>

              <td>
                {coin.whales}
              </td>

              <td>
                {coin.age}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}