import { useEffect, useState } from "react";

export default function Dashboard() {

  const [coins, setCoins] = useState([]);

  useEffect(() => {

    fetch("https://your-backend/scan")
      .then(r => r.json())
      .then(setCoins);

  }, []);

  return (

    <div>

      <h1>
        📊 Dashboard
      </h1>

      {coins.map((c, i) => (

        <div key={i}>

          {c.token} - {c.score}

        </div>

      ))}

    </div>
  );
}