const API_URL =
  "https://crypto-saas-v2.onrender.com/api/tokens";

async function loadTokens() {

  try {

    document.getElementById(
      "status"
    ).innerHTML =
      "⚡ Predictive Sniper AI Online";

    const response = await fetch(API_URL);

    const data = await response.json();

    const table =
      document.getElementById("tokenTable");

    table.innerHTML = "";

    data.forEach((coin) => {

      table.innerHTML += `
        <tr>
          <td>${coin.type}</td>

          <td>
            <a href="${coin.url}"
               target="_blank">
               ${coin.symbol}
            </a>
          </td>

          <td>$${coin.price}</td>

          <td>${coin.priceChange}%</td>

          <td>$${coin.liquidity}</td>

          <td>$${coin.volume}</td>

          <td><b>${coin.score}</b></td>

          <td>${coin.rating}</td>

          <td><b>${coin.risk}</b></td>

          <td>${coin.signal}</td>

          <td>${coin.confidence}</td>

          <td>${coin.whales}</td>

          <td>${coin.age}</td>
        </tr>
      `;
    });

  } catch (err) {

    console.log(err);

    document.getElementById(
      "status"
    ).innerHTML =
      "❌ Backend connection failed";
  }
}

loadTokens();

setInterval(loadTokens, 15000);