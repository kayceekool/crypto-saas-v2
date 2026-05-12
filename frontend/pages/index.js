const API = "https://YOUR-BACKEND.onrender.com/scan";

let lastGoodData = [];
let loading = false;

async function loadScanner() {

    // prevent overlapping calls
    if (loading) {
        return;
    }

    loading = true;

    try {

        const response = await fetch(API);

        const data = await response.json();

        // =========================
        // 🧠 KEEP LAST GOOD DATA
        // =========================

        if (
            data &&
            data.scanner &&
            data.scanner.length > 0
        ) {
            lastGoodData = data.scanner;
        }

        const scanner = lastGoodData;

        const table = document.getElementById("scanner-body");

        const count = document.getElementById("token-count");

        if (!table) {
            loading = false;
            return;
        }

        table.innerHTML = "";

        count.innerText = scanner.length;

        scanner.forEach((token) => {

            const row = document.createElement("tr");

            // =========================
            // 🎨 SIGNAL COLORS
            // =========================

            let signalColor = "white";

            if (token.signal === "PARABOLIC") {
                signalColor = "#00ff99";
            }

            else if (token.signal === "SNIPER ENTRY") {
                signalColor = "#00ccff";
            }

            else if (token.signal === "BUY") {
                signalColor = "orange";
            }

            row.innerHTML = `
                <td>${token.type}</td>

                <td>
                    <a href="${token.url}" target="_blank">
                        ${token.name}
                    </a>
                </td>

                <td>$${token.price}</td>

                <td>${token.change}%</td>

                <td>$${Number(token.liquidity).toLocaleString()}</td>

                <td>$${Number(token.volume).toLocaleString()}</td>

                <td><b>${token.score}</b></td>

                <td>${token.rating}</td>

                <td><b>${token.risk}</b></td>

                <td style="color:${signalColor};font-weight:bold;">
                    ${token.signal}
                </td>

                <td>${token.confidence}</td>

                <td>${token.whales}</td>

                <td>${token.age}</td>
            `;

            table.appendChild(row);
        });

        document.getElementById("status").innerText =
            "⚡ AI engine online";

    } catch (err) {

        console.log(err);

        // keep previous data visible
        document.getElementById("status").innerText =
            "🟡 Reconnecting AI engine...";
    }

    loading = false;
}

// first load
loadScanner();

// stable refresh
setInterval(loadScanner, 30000);
```javascript
const API = "https://YOUR-BACKEND.onrender.com/scan";

async function loadScanner() {

    try {

        const response = await fetch(API);

        const data = await response.json();

        const scanner = data.scanner || [];

        const table = document.getElementById("scanner-body");

        const count = document.getElementById("token-count");

        table.innerHTML = "";

        count.innerText = scanner.length;

        scanner.forEach((token) => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${token.type}</td>

                <td>
                    <a href="${token.url}" target="_blank">
                        ${token.name}
                    </a>
                </td>

                <td>$${token.price}</td>

                <td>${token.change}%</td>

                <td>$${Number(token.liquidity).toLocaleString()}</td>

                <td>$${Number(token.volume).toLocaleString()}</td>

                <td><b>${token.score}</b></td>

                <td>${token.rating}</td>

                <td><b>${token.risk}</b></td>

                <td>${token.signal}</td>

                <td>${token.confidence}</td>

                <td>${token.whales}</td>

                <td>${token.age}</td>
            `;

            table.appendChild(row);
        });

        document.getElementById("status").innerText =
            "⚡ AI engine online";

    } catch (err) {

        console.log(err);

        document.getElementById("status").innerText =
            "❌ Backend connection failed";
    }
}

loadScanner();

setInterval(loadScanner, 20000);