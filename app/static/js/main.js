document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById("search-leads");
    const endpoint_search = "/api/leads";
    const endpoint_history = "/api/history";

    function remove_rows() {
        const rows = document.querySelectorAll(".generated");
        for (const row of rows) row.remove();
    }

    function remove_visits() {
        const historyRows = document.querySelectorAll(".history-row");
        for (const row of historyRows) row.remove();
    }

    function add_rows(lead_data) {
        for (const lead of lead_data) {
            const tableBody = document.getElementById("table-body");
            const tableRow = tableBody.insertRow(-1);
            tableRow.classList.add("generated");
            const emailCol = tableRow.insertCell(0);
            const nameCol = tableRow.insertCell(1);
            const phoneCol = tableRow.insertCell(2);
            const historyCol = tableRow.insertCell(3);

            emailCol.appendChild(document.createTextNode(lead.email));
            nameCol.appendChild(document.createTextNode(lead.name));
            phoneCol.appendChild(document.createTextNode(lead.phone));

            const historyButton = document.createElement("button");
            historyButton.classList.add("button-history");
            historyButton.value = lead.id;
            historyButton.appendChild(document.createTextNode("History"));
            historyCol.appendChild(historyButton);
        }
    }

    function add_visits(visits_data, parent) {
        const historyRow = document.createElement("tr");
        historyRow.classList.add("history-row");
        const historyData = document.createElement("td");
        historyData.colSpan = 4;
        const divExt = document.createElement("div");
        divExt.classList.add("div-ext", "p-3");
        const div = document.createElement("div");
        div.classList.add("visits-div", "p-3");
        const table = document.createElement("table");
        table.classList.add("visits-table");
        const titleRow = table.insertRow(-1);
        titleRow.classList.add("visits-head-row");
        const title = document.createElement("th");
        title.appendChild(document.createTextNode("Log de Acessos:"));
        titleRow.appendChild(title);
        div.appendChild(table);
        divExt.appendChild(div);
        historyData.appendChild(divExt);
        historyRow.appendChild(historyData);
        parent.parentNode.insertBefore(historyRow, parent.nextSibling);

        for (const visit of visits_data) {
            const visitRow = table.insertRow(-1);
            visitRow.classList.add("visits-row");
            const dateCol = visitRow.insertCell(-1);
            const ssidCol = visitRow.insertCell(-1);
            dateCol.appendChild(document.createTextNode(visit.created_at.replace("T", " ")));
            ssidCol.appendChild(document.createTextNode(visit.ssid));
        }
    }

    async function fetchSearch() {
        try {
            const params = new URLSearchParams({search: searchInput.value});
            const response = await fetch(`${endpoint_search}?${params}`);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            remove_rows();
            remove_visits();

            if (data[0]["error"]) {
                if (data[0]["error"] == "no_result") {
                    add_rows([{"email": "No result", "name": "No result", "phone": "No result"}]);
                } else if (data[0]["error"] == "over_max_length") {
                    add_rows([{"email": "Over max lenght", "name": "Over max lenght", "phone": "Over max lenght"}]);
                }
            } else {
                add_rows(data);
                historyListener();
            }
        } catch (error) {
            console.error('Fetch failed:', error);
        }
    }

    async function fetchHistory(value, parent) {
        try {
            const params = new URLSearchParams({lead_id: value});
            const response = await fetch(`${endpoint_history}?${params}`);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            if (!data[0]["error"]) add_visits(data, parent);
        } catch (error) {
            console.error('Fetch failed:', error);
        }
    }

    function historyListener() {
        const historyList = document.querySelectorAll(".button-history");
        for (const historyButton of historyList) {
            historyButton.addEventListener("click", () => {
                const parent = historyButton.closest("tr");
                const nextElement = parent.nextElementSibling;
                if (nextElement && nextElement.classList.contains("history-row")) {
                    const divExt = nextElement.querySelector(".div-ext");
                    divExt.style.height = `${divExt.scrollHeight}px`;
                    void divExt.offsetHeight;
                    divExt.addEventListener("transitionend", (event) => {
                        if (event.target === divExt && event.propertyName === "height") nextElement.remove();
                    });
                    divExt.style.height = "30px";
                    divExt.style.opacity = "0";
                } else {
                    fetchHistory(historyButton.value, parent);
                }
            });
        }
    }

    function debounce(func, timeout = 500) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => { func.apply(this, args); }, timeout);
        };
    }

    searchInput.addEventListener("input", debounce(() => fetchSearch()));
    historyListener();
});
