// =========================================================
// SOC DASHBOARD
// =========================================================

async function loadEvents() {

    try {

        const response = await fetch("/api/events");

        if (!response.ok) {
            throw new Error("Failed to fetch events");
        }

        const data = await response.json();

        const events = data.events || [];

        updateStats(events);

        updateTable(events);

        updateActivity(events);

        document.getElementById("last-updated").textContent =
            "Last updated: " + new Date().toLocaleTimeString();

    } catch (error) {

        console.error("Error loading events:", error);

        document.getElementById("events-table").innerHTML = `
            <tr>
                <td colspan="7" class="loading">
                    Unable to load security events
                </td>
            </tr>
        `;
    }
}


// =========================================================
// UPDATE STATISTICS
// =========================================================

function updateStats(events) {

    const totalEvents = events.length;

    const highEvents = events.filter(
        event => event.severity === "high"
    ).length;

    const failedAuth = events.filter(
        event => event.event === "Failed Authentication"
    ).length;

    const unauthorized = events.filter(
        event =>
            event.event === "Unauthorized Request" ||
            event.event === "Forbidden Request"
    ).length;


    document.getElementById("total-events").textContent =
        totalEvents;

    document.getElementById("high-events").textContent =
        highEvents;

    document.getElementById("failed-auth").textContent =
        failedAuth;

    document.getElementById("unauthorized").textContent =
        unauthorized;
}


// =========================================================
// UPDATE ACTIVITY BARS
// =========================================================

function updateActivity(events) {

    const total = events.length;

    const high = events.filter(
        event => event.severity === "high"
    ).length;


    const eventPercentage =
        total > 0 ? 100 : 0;

    const highPercentage =
        total > 0 ? (high / total) * 100 : 0;


    document.getElementById("activity-events").style.width =
        eventPercentage + "%";

    document.getElementById("activity-high").style.width =
        highPercentage + "%";
}


// =========================================================
// UPDATE EVENTS TABLE
// =========================================================

function updateTable(events) {

    const table = document.getElementById("events-table");

    if (events.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="7" class="loading">
                    No security events found
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML = "";


    // Show newest events first
    const recentEvents = [...events].reverse().slice(0, 50);


    recentEvents.forEach(event => {

        const row = document.createElement("tr");


        // Convert Loki timestamp
        let timestamp = event.timestamp;

        try {

            timestamp = new Date(
                Number(event.timestamp) / 1000000
            ).toLocaleString();

        } catch {
            // Keep original timestamp
        }


        const severity = (
            event.severity || "info"
        ).toLowerCase();


        const category = (
            event.category || "System"
        );


        const status =
            event.status !== undefined
                ? event.status
                : "-";


        const statusClass =
            getStatusClass(status);


        row.innerHTML = `
            <td>
                ${escapeHTML(timestamp)}
            </td>

            <td>
                ${escapeHTML(event.source || "-")}
            </td>

            <td>
                <span class="category-badge">
                    ${escapeHTML(category)}
                </span>
            </td>

            <td>
                ${escapeHTML(event.event || "-")}
            </td>

            <td>
                <span class="status-badge ${statusClass}">
                    ${escapeHTML(status)}
                </span>
            </td>

            <td class="path-cell">
                ${escapeHTML(event.path || "-")}
            </td>

            <td>
                <span class="severity-badge severity-${severity}">
                    ${severity.toUpperCase()}
                </span>
            </td>
        `;


        table.appendChild(row);

    });
}


// =========================================================
// STATUS BADGE
// =========================================================

function getStatusClass(status) {

    if (status === 401 || status === 403) {
        return "status-danger";
    }

    if (status === 404) {
        return "status-warning";
    }

    if (status === 302) {
        return "status-auth";
    }

    if (status >= 200 && status < 300) {
        return "status-success";
    }

    if (status >= 300 && status < 400) {
        return "status-info";
    }

    return "status-neutral";
}


// =========================================================
// HTML SAFETY
// =========================================================

function escapeHTML(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


// =========================================================
// REFRESH BUTTON
// =========================================================

document
    .getElementById("refresh-btn")
    .addEventListener("click", loadEvents);


// =========================================================
// INITIAL LOAD
// =========================================================

loadEvents();


// =========================================================
// AUTO REFRESH
// =========================================================

// Refresh every 10 seconds
setInterval(loadEvents, 10000);
