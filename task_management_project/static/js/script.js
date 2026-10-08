// Shared helper functions used by every page

// Call the backend API and return { ok, status, data }
async function apiRequest(url, method = "GET", body = null) {
    const options = {
        method: method,
        headers: { "Content-Type": "application/json" }
    };

    // Send the login token if we have one (DRF format: "Token <key>")
    const token = localStorage.getItem("token");
    if (token) {
        options.headers["Authorization"] = "Token " + token;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    // DELETE returns 204 (no content), so there may be no JSON to read
    let data = {};
    if (response.status !== 204) {
        data = await response.json();
    }

    // Token is missing or expired -> go back to login
    if (response.status === 401 && !url.includes("/api/login/")) {
        logoutLocal();
    }

    return { ok: response.ok, status: response.status, data: data };
}

// Turn a DRF error response into one readable line.
// DRF errors look like: {"title": ["This field may not be blank."]}
function getErrorText(data) {
    if (data.error) return data.error;
    if (data.detail) return data.detail;

    const messages = [];
    for (const field in data) {
        messages.push(field + ": " + data[field].join(" "));
    }
    return messages.join(" | ") || "Something went wrong";
}

// Redirect to login page if user is not logged in
function requireLogin() {
    if (!localStorage.getItem("token")) {
        window.location.href = "/";
    }
}

function logoutLocal() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "/";
}

async function logout() {
    await apiRequest("/api/logout/", "POST");
    logoutLocal();
}

// Show a red or green message box
function showMessage(elementId, text, type = "danger") {
    const box = document.getElementById(elementId);
    box.className = "alert alert-" + type;
    box.textContent = text;
}

// Read a value from the URL, e.g. ?id=5
function getUrlParam(name) {
    return new URLSearchParams(window.location.search).get(name);
}

// Colored badge for status / priority
function statusBadge(status) {
    const colors = { "Todo": "secondary", "In Progress": "primary", "Completed": "success" };
    return `<span class="badge bg-${colors[status]}">${status}</span>`;
}

function priorityBadge(priority) {
    const colors = { "Low": "info", "Medium": "warning", "High": "danger" };
    return `<span class="badge bg-${colors[priority]} text-dark">${priority}</span>`;
}

// Prevent HTML injection when showing user text
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text || "";
    return div.innerHTML;
}
