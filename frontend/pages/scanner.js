import { useEffect, useState } from "react";

export default function Scanner() {

  const [coins, setCoins] = useState([]);
  const [status, setStatus] = useState("Loading sniper scanner...");

  async function loadScanner() {

    try {

      const res = await fetch(
        "https://crypto-saas-v2.onrender.com/scan"
      );

      const data = await res.json();

      if (Array.isArray(data)) {

        setCoins(data);

        setStatus(`🔥 Live Sniper Scanner • ${data.length} tokens`);

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

    const interval = setInterval(loadScanner, 15000);

    return () => clearInterval(interval);

  }, []);

  return (

    <div style={{ padding: 20, background: "#050505", color: "#fff", minHeight: "100vh" }}>

      <h1>🚀 SNIPER TEST VERSION</h1>

      <p style={{ color: "#00ffaa" }}>{status}</p>

      <table style={{ width: "100%", marginTop: 20 }}>

        <thead>
          <tr>
            <th>Token</th>
            <th>Price</th>
            <th>24h %</th>
          </tr>
        </thead>

        <tbody>

          {coins.map((coin, i) => (

            <tr key={i}>

              <td>{coin.name}</td>

              <td>
                {coin.price > 0
                  ? `$${Number(coin.price).toLocaleString()}`
                  : "NEW"}
              </td>

              <td style={{ color: coin.change >= 0 ? "#00ff99" : "red" }}>
                {coin.change}%
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}