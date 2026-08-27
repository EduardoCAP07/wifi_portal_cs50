document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById("search-leads");
    const endpoint_search = "/api/leads";

    function remove_rows() {
        const rows = document.querySelectorAll(".generated");

        for (const row of rows) {
            row.remove();
        }
    }

    function add_rows(lead_data) {
        for (const lead of lead_data) {
            const tableBody = document.getElementById("table-body");
            const tableRow = tableBody.insertRow(-1);
            tableRow.classList.add("generated");
            const emailCol = tableRow.insertCell(0);
            const nameCol = tableRow.insertCell(1);
            const phoneCol = tableRow.insertCell(2);

            emailCol.appendChild(document.createTextNode(lead.email));
            nameCol.appendChild(document.createTextNode(lead.name));
            phoneCol.appendChild(document.createTextNode(lead.phone));
        }
    }

    async function fetchSearch() {
        try {
            const search = searchInput.value;
            const params = new URLSearchParams({
                search: search
            });
            const url = `${endpoint_search}?${params}`;
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            remove_rows();

            if (data[0]["error"]) {
                if (data[0]["error"] == "no_result") {
                    const noResult = [{"email": "No result", "name": "No result", "phone": "No result"}];
                    add_rows(noResult);
                } else if (data[0]["error"] == "over_max_length") {
                    const overMaxLenght = [{"email": "Over max lenght", "name": "Over max lenght", "phone": "Over max lenght"}];
                    add_rows(overMaxLenght);
                }
            } else {
                add_rows(data);
            }
        } catch (error) {
            console.error('Fetch failed:', error);
        }
    }

    function debounce(func, timeout = 500) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => { func.apply(this, args); }, timeout);
        };
    }

    const processChange = debounce(() => fetchSearch());
    searchInput.addEventListener("input", processChange);
});
