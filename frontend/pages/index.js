// =========================================
// 🚀 ELITE FRONTEND ENGINE v33
// =========================================

const API_URL =
  "https://crypto-saas-v2.onrender.com/scan";

const tbody =
  document.getElementById("scannerBody");

const liveStatus =
  document.getElementById("liveStatus");

// =========================================
// 🔥 STATUS ENGINE
// =========================================

const statusMessages = [

  "Scanning whale wallets...",

  "Tracking smart money...",

  "Analyzing momentum...",

  "Filtering fake pumps...",

  "Detecting sniper entries...",

  "Monitoring liquidity inflows...",

  "Institutional AI active...",

  "Syncing live market data...",

  "Watching meme rotations...",

  "Calculating confidence engine..."
];

let statusIndex = 0;

setInterval(() => {

  if (liveStatus) {

    liveStatus.innerText =
      statusMessages[statusIndex];

    statusIndex++;

    if (
      statusIndex >=
      statusMessages.length
    ) {
      statusIndex = 0;
    }
  }

}, 4000);

// =========================================
// 🎨 SCORE COLORS
// =========================================

function getScoreClass(score) {

  if (score >= 900)
    return "score-god";

  if (score >= 650)
    return "score-para";

  if (score >= 350)
    return "score-gem";

  return "score-normal";
}

// =========================================
// 🚀 LOAD SCANNER
// =========================================

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

      const scoreClass =
        getScoreClass(token.score);

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

        <td class="${scoreClass}">
          <b>${token.score}</b>
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

// =========================================
// 🔄 AUTO REFRESH
// =========================================

loadScanner();

setInterval(
  loadScanner,
  15000
);