// =========================
// 🚀 FULL UPGRADED index.js
// =========================

async function loadScanner() {

    try {

        document.getElementById(
            "status"
        ).innerHTML =
            "Syncing live market data...";

        const response = await fetch(
            "https://crypto-saas-v2.onrender.com/scan"
        );

        const data = await response.json();

        const scanner = data.scanner || [];

        let html = `

        <h1>🚀 CRYPTO SCANNER</h1>

        <p>
            🔥 Live Sniper AI •
            ${scanner.length} tokens
        </p>

        <p>⚡ AI engine online</p>

        <table>

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
                <th>Trend</th>
                <th>Virality</th>
                <th>Entry</th>

            </tr>
        `;

        scanner.forEach(token => {

            html += `

            <tr>

                <td>${token.type}</td>

                <td>
                    <a href="${token.url}"
                       target="_blank">

                        ${token.name}

                    </a>
                </td>

                <td>$${token.price}</td>

                <td>${token.change}%</td>

                <td>$${token.liquidity}</td>

                <td>$${token.volume}</td>

                <td><b>${token.score}</b></td>

                <td>${token.rating}</td>

                <td><b>${token.risk}</b></td>

                <td>${token.signal}</td>

                <td>${token.confidence}</td>

                <td>${token.whales}</td>

                <td>${token.age}</td>

                <td>${token.trend}</td>

                <td>${token.virality}</td>

                <td>${token.entry}</td>

            </tr>
            `;
        });

        html += `</table>`;

        document.getElementById(
            "app"
        ).innerHTML = html;

        document.getElementById(
            "status"
        ).innerHTML =
            "✅ Live scanner stable";

    } catch (err) {

        document.getElementById(
            "status"
        ).innerHTML =
            "⚠️ Backend connection failed";
    }
}

loadScanner();

setInterval(() => {

    loadScanner();

}, 15000);