import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    fetch("https://crypto-saas-v2.onrender.com")
      .then(res => res.json())
      .then(data => setMessage(data.status || data.message))
      .catch(() => setMessage("Backend connection failed"));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚀 Crypto SaaS Live</h1>
      <p><strong>Backend Response:</strong> {message}</p>
    </div>
  );
}