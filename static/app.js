const tableBody = document.getElementById("inventory-table-body");
const inventoryMessage = document.getElementById("inventory-message");
const searchResults = document.getElementById("search-results");

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || `Request failed (${response.status})`);
    }

    return data;
}

function showMessage(message) {
    inventoryMessage.textContent = message;
}

async function loadInventory() {
    showMessage("Loading inventory...");
    tableBody.replaceChildren();

    try {
        const items = await apiRequest("/inventory");

        if (!Array.isArray(items) || items.length === 0) {
            showMessage("No inventory items found.");
            return;
        }

        items.forEach((item) => {
            const row = document.createElement("tr");

            [
                item.id,
                item.name,
                item.category,
                item.quantity,
                Number(item.price).toFixed(2)
            ].forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "";
                row.appendChild(cell);
            });

            const actions = document.createElement("td");
            const editButton = document.createElement("button");
            editButton.textContent = "Edit";
            editButton.className = "button action-button";
            editButton.type = "button";
            editButton.addEventListener("click", () => editItem(item));

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "button secondary action-button";
            deleteButton.type = "button";
            deleteButton.addEventListener("click", () => deleteItem(item.id));

            actions.append(editButton, deleteButton);
            row.appendChild(actions);
            tableBody.appendChild(row);
        });

        showMessage(`${items.length} inventory item(s) loaded.`);
    } catch (error) {
        showMessage(error.message);
    }
}

async function editItem(item) {
    const name = prompt("Product name:", item.name);
    if (name === null) return;

    const category = prompt("Category:", item.category);
    if (category === null) return;

    const quantityText = prompt("Quantity:", item.quantity);
    if (quantityText === null) return;

    const priceText = prompt("Price:", item.price);
    if (priceText === null) return;

    const quantity = Number(quantityText);
    const price = Number(priceText);

    if (
        !name.trim() ||
        !category.trim() ||
        !Number.isInteger(quantity) ||
        quantity < 0 ||
        !Number.isFinite(price) ||
        price < 0
    ) {
        alert("Enter a name, category, whole non-negative quantity, and valid non-negative price.");
        return;
    }

    try {
        await apiRequest(`/inventory/${item.id}`, {
            method: "PATCH",
            body: JSON.stringify({ name, category, quantity, price })
        });
        await loadInventory();
    } catch (error) {
        alert(error.message);
    }
}

async function deleteItem(id) {
    if (!confirm(`Delete inventory item ${id}?`)) return;

    try {
        await apiRequest(`/inventory/${id}`, { method: "DELETE" });
        await loadInventory();
    } catch (error) {
        alert(error.message);
    }
}

document.getElementById("refresh-button").addEventListener("click", loadInventory);

document.getElementById("add-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const form = new FormData(event.currentTarget);
    const payload = {
        name: form.get("name").trim(),
        category: form.get("category").trim(),
        quantity: Number(form.get("quantity")),
        price: Number(form.get("price"))
    };

    try {
        await apiRequest("/inventory", {
            method: "POST",
            body: JSON.stringify(payload)
        });
        event.currentTarget.reset();
        await loadInventory();
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById("search-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = document.getElementById("search-name").value.trim();
    searchResults.textContent = "Searching...";

    try {
        const products = await apiRequest(
            `/products/search?name=${encodeURIComponent(name)}`
        );
        searchResults.textContent = JSON.stringify(products, null, 2);
    } catch (error) {
        searchResults.textContent = error.message;
    }
});

document.getElementById("barcode-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const barcode = document.getElementById("barcode").value.trim();
    searchResults.textContent = "Looking up barcode...";

    try {
        const product = await apiRequest(
            `/products/barcode/${encodeURIComponent(barcode)}`
        );
        searchResults.textContent = JSON.stringify(product, null, 2);
    } catch (error) {
        searchResults.textContent = error.message;
    }
});

loadInventory();
