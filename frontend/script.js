window.onload = function () {

    // attacca event listener dopo che il DOM è caricato
    document.getElementById("modeSelect")
        .addEventListener("change", updateUIBasedOnMode);

    updateUIBasedOnMode();
    embedThoughtSpot();
};


function embedThoughtSpot() {

    const { init, SearchEmbed, AuthType } = window.tsembed;

    init({
        thoughtSpotHost: "https://techpartners.thoughtspot.cloud",
//        authType: AuthType.None,
        authType: AuthType.TrustedAuthTokenCookieless,
        getAuthToken: async () => {
            const res = await fetch("http://127.0.0.1:8000/api/ts-token", {
                headers: {
                    "Authorization": `Bearer ${accessToken}`
                }
            });
            return await res.text();
        }

    });

    // SearchEmbed mostra tutta l'interfaccia completa di TS dati + query
    // LiveboardEmbed mostra una dashboard specifica, niente search UI
    // VisualizationEmbed mostra un singolo grafico
    const embed = new SearchEmbed(
        document.getElementById("ts-container")
    );

    embed.render();
}


function updateUIBasedOnMode() {
    const mode = document.getElementById("modeSelect").value;

    const loginSection = document.getElementById("login-section");
    const userSection = document.getElementById("user-section");

    if (mode === "app") {
        // App owns data
        loginSection.style.display = "none";   // nasconde login
        userSection.style.display = "block";   // mostra select utente

    } else {
        // User owns data
        loginSection.style.display = "block";  // mostra login
        userSection.style.display = "none";    // nasconde select utente
    }
}

const msalConfig = {
    auth: {
        clientId: "599af31d-a5ad-4cef-ae5d-b3f4b51d1e66",
        authority: "https://login.microsoftonline.com/c9c4d101-2487-4a99-bce1-d9079d8d573a",
        redirectUri: "http://localhost:5500"
    }
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

let currentAccount = null;
let accessToken = null;

async function login() {
    try {
        console.log("LOGIN CLICK");  // debug

        const loginResponse = await msalInstance.loginPopup({
            scopes: ["api://599af31d-a5ad-4cef-ae5d-b3f4b51d1e66/access_as_user"]
        });

        console.log("LOGIN RESPONSE:", loginResponse);

        currentAccount = loginResponse.account;

        const tokenResponse = await msalInstance.acquireTokenSilent({
            account: currentAccount,
            scopes: ["api://599af31d-a5ad-4cef-ae5d-b3f4b51d1e66/access_as_user"]
        });

        accessToken = tokenResponse.accessToken;

        console.log("ACCESS TOKEN:", accessToken);
        console.log("USER:", currentAccount);

        document.getElementById("auth-status").innerHTML =
            `<strong>Logged in as:</strong> ${currentAccount.username}`;

    } catch (error) {
        console.error("LOGIN ERROR:", error);
    }
}


async function loadReport() {
    const user = document.getElementById("userSelect").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Loading...";

    try {
        let response;

        if (accessToken) {
            // USER OWNS DATA
            // local -> http://127.0.0.1:8000/api/embed-info
            response = await fetch(`http://127.0.0.1:8000/api/embed-info`, {
                method: "POST",
                headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${accessToken}`
                    },
                body: JSON.stringify({})
            });
        } else {
            // APP OWNS DATA
            response = await fetch(`http://127.0.0.1:8000/api/embed-info?user=${user}`);
        }

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();

        const embedInfo = data.embedInfo;

        resultDiv.innerHTML = `
            <h3>Backend response</h3>
            <strong>User:</strong> ${data.user}<br>
        `;

        embedPowerBIReport(embedInfo);

    } catch (error) {
        resultDiv.innerHTML = `<span style="color:red;">Error: ${error.message}</span>`;
    }
}

function embedPowerBIReport(embedInfo) {
    const container = document.getElementById("report-container");

    // Rimuove eventuali embed precedenti
    powerbi.reset(container);

    // Caso con token fake
    if (embedInfo.accessToken.startsWith("FAKE_TOKEN")) {
        container.innerHTML = `
            <div>
                <p><strong>Power BI Embedded placeholder</strong></p>
                <p>Report ID: ${embedInfo.reportId}</p>
                <p>Customer ID (CustomData): ${embedInfo.securityContext.customer_id}</p>
                <p style="color: #999;">
                    Power BI Embedded will be activated when capacity is available
                </p>
            </div>
        `;
        return;
    }

    // Caso con token reale
    const models = window['powerbi-client'].models;

    const config = {
        type: 'report',
        tokenType: models.TokenType.Aad,
        accessToken: embedInfo.accessToken,
        embedUrl: embedInfo.embedUrl,
        id: embedInfo.reportId,
        permissions: models.Permissions.All,
        settings: {
            panes: {
                filters: { visible: true },
                pageNavigation: { visible: true }
            }
        }
    };

    const report = powerbi.embed(container, config);
    window.report = report;
}


async function applyFilters() {
    const country = document.getElementById("country").value;
    const year = document.getElementById("year").value;

    const filters = [];

    if (country) {
        filters.push({
            $schema: "http://powerbi.com/product/schema#basic",
            target: {
                table: "Sales",        // esempio
                column: "Country"     // esempio
            },
            operator: "In",
            values: [country]
        });
    }

    if (year) {
        filters.push({
            $schema: "http://powerbi.com/product/schema#basic",
            target: {
                table: "Sales",
                column: "Year"
            },
            operator: "In",
            values: [year]
        });
    }

    // Applicazione filtri al report
    const report = window.report;
    await report.setFilters(filters);
}


async function clearFilters() {
    if (!window.report) {
        console.log("Report non pronto");
        return;
    }

    await window.report.setFilters([]);

    // reset UI
    document.getElementById("country").value = "";
    document.getElementById("year").value = "";
}



