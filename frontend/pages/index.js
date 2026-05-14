// ================================
// 🚀 FULL UPGRADED index.js
// Upgrades 11 → 22 Integrated
// ================================

const API_URL = "https://crypto-saas-v2.onrender.com/scan";

const tbody = document.getElementById("scannerBody");

const liveStatus = document.getElementById("liveStatus");

// =========================
// 🔥 LIVE STATUS ENGINE
// =========================

const statusMessages = [
  "Scanning whale wallets...",
  "Tracking smart money...",
  "Analyzing momentum...",
  "Filtering fake pumps...",
  "Monitoring parabolic tokens...",
  "Detecting sniper entries...",
  "Syncing live market data...",
  "AI confidence recalculating...",
  "Watching liquidity inflows...",
  "Institutional engine active..."
];

let statusIndex = 0;

setInterval(() => {

  const el = document.getElementById("liveStatus");

  if (el) {

    el.innerText = statusMessages[statusIndex];

    statusIndex++;

    if (statusIndex >= statusMessages.length) {
      statusIndex = 0;
    }
  }

}, 4000);

// =========================
// 🚀 RENDER ENGINE
// =========================

async function loadScanner() {

  try {

    const response = await fetch(API_URL);

    const data = await response.json();

    tbody.innerHTML = "";

    data.forEach(token => {

      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${token.type}</td>

        <td>
          <a href="${token.url}" target="_blank">
            ${token.symbol}
          </a>
        </td>

        <td>$${token.price}</td>

        <td>${token.priceChange}%</td>

        <td>$${token.liquidity.toLocaleString()}</td>

        <td>$${token.volume.toLocaleString()}</td>

        <td><b>${token.score}</b></td>

        <td>${token.rating}</td>

        <td>${token.risk}</td>

        <td>${token.signal}</td>

        <td>${token.confidence}%</td>

        <td>${token.whales}</td>

        <td>${token.age}</td>
      `;

      tbody.appendChild(row);

    });

  } catch (err) {

    console.log(err);

  }
}

// =========================
// 🚀 AUTO REFRESH
// =========================

loadScanner();

setInterval(loadScanner, 15000);