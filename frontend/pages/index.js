// ================================
// 🚀 FULL UPGRADED index.js
// Upgrades 23 → 33 Integrated
// ================================

const API_URL =
"https://crypto-saas-v2.onrender.com/scan";

const tbody =
document.getElementById("scannerBody");

// =========================
// LIVE STATUS
// =========================

const statusMessages = [

  "Scanning whale wallets...",
  "Tracking smart money...",
  "Detecting mega breakouts...",
  "Monitoring liquidity shifts...",
  "Analyzing AI momentum...",
  "Watching elite whale inflows...",
  "Filtering rugpull risks...",
  "Monitoring sniper entries...",
  "AI institutional engine active...",
  "Live market synchronization..."

];

let statusIndex = 0;

setInterval(() => {

  const liveStatus =
  document.getElementById("liveStatus");

  if (liveStatus) {

    liveStatus.innerText =
    statusMessages[statusIndex];

    statusIndex++;

    if (statusIndex >= statusMessages.length) {
      statusIndex = 0;
    }

  }

}, 3500);

// =========================
// LOAD SCANNER
// =========================

async function loadScanner() {

  try {

    const response =
    await fetch(API_URL);

    const data =
    await response.json();

    tbody.innerHTML = "";

    data.forEach(token => {

      const row =
      document.createElement("tr");

      let scoreColor = "";

      if (token.score >= 1200) {
        scoreColor = "#ff00ff";
      }
      else if (token.score >= 900) {
        scoreColor = "#ff0000";
      }
      else if (token.score >= 700) {
        scoreColor = "#ff8800";
      }
      else {
        scoreColor = "#00ff99";
      }

      row.innerHTML = `

        <td>${token.type}</td>

        <td>
          <a href="${token.url}"
          target="_blank">
          ${token.symbol}
          </a>
        </td>

        <td>$${token.price}</td>

        <td>${token.priceChange}%</td>

        <td>$${token.liquidity.toLocaleString()}</td>

        <td>$${token.volume.toLocaleString()}</td>

        <td>
          <b style="
            color:${scoreColor};
            font-size:16px;
          ">
            ${token.score}
          </b>
        </td>

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
// AUTO REFRESH
// =========================

loadScanner();

setInterval(loadScanner, 12000);