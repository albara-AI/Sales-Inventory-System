const API_BASE = "";

// Utils
function formatCurrency(num) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);
}

// Admin: Dashboard
async function loadDashboardStats() {
    try {
        const res = await fetch(`${API_BASE}/reports/dashboard`);
        const data = await res.json();

        const revEl = document.getElementById('total-revenue');
        const ordEl = document.getElementById('total-orders');

        if (revEl) revEl.textContent = formatCurrency(data.summary.total_revenue);
        if (ordEl) ordEl.textContent = data.summary.total_orders;
    } catch (e) {
        console.error("Failed to load stats", e);
    }
}

// Admin: Products
async function loadProducts() {
    const tbody = document.getElementById('products-body');
    if (!tbody) return; // Not on admin page or product table missing

    tbody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>';

    try {
        const res = await fetch(`${API_BASE}/products/`);
        const products = await res.json();

        tbody.innerHTML = '';
        products.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.product_id}</td>
                <td>${p.name}</td>
                <td>${p.sku}</td>
                <td>${formatCurrency(p.unit_price)}</td>
                <td>
                    <button onclick="editProduct(${p.product_id})" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Edit</button>
                    <button onclick="deleteProduct(${p.product_id})" class="btn btn-danger" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="5">Error loading products</td></tr>';
    }
}

let isEditing = false;

function showAddProductModal() {
    isEditing = false;
    document.getElementById('product-form').reset();
    document.getElementById('prod-id').value = '';
    document.getElementById('product-modal').style.display = 'flex';
}

async function editProduct(id) {
    isEditing = true;
    try {
        const res = await fetch(`${API_BASE}/products/${id}`);
        const p = await res.json();

        document.getElementById('prod-id').value = p.product_id;
        document.getElementById('prod-name').value = p.name;
        document.getElementById('prod-sku').value = p.sku;
        document.getElementById('prod-price').value = p.unit_price;

        document.getElementById('product-modal').style.display = 'flex';
    } catch (e) {
        alert("Failed to fetch product details");
    }
}

function closeModal() {
    document.getElementById('product-modal').style.display = 'none';
}

async function handleSaveProduct(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        name: formData.get('name'),
        sku: formData.get('sku'),
        unit_price: parseFloat(formData.get('unit_price')),
        description: ""
    };

    const id = formData.get('product_id');
    const method = isEditing ? "PUT" : "POST";
    const url = isEditing ? `${API_BASE}/products/${id}` : `${API_BASE}/products/`;

    try {
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            closeModal();
            loadProducts();
        } else {
            alert("Error saving product");
        }
    } catch (e) {
        console.error(e);
        alert("Error saving product");
    }
}

async function deleteProduct(id) {
    if (!confirm("Are you sure?")) return;
    try {
        await fetch(`${API_BASE}/products/${id}`, { method: "DELETE" });
        loadProducts();
    } catch (e) {
        alert("Error deleting");
    }
}

// Admin: Inventory
function switchTab(tab) {
    document.getElementById('products-section').style.display = tab === 'products' ? 'block' : 'none';
    document.getElementById('inventory-section').style.display = tab === 'inventory' ? 'block' : 'none';
}

async function loadWarehouses() {
    const list = document.getElementById('warehouse-list');
    if (!list) return;
    const res = await fetch(`${API_BASE}/inventory/warehouses`);
    const warehouses = await res.json();
    list.innerHTML = warehouses.map(w => `<li style="padding: 0.5rem; border-bottom: 1px solid #eee;"><b>${w.warehouse_id}:</b> ${w.name} (${w.location})</li>`).join('');
}

async function showAddWarehouseModal() {
    const name = prompt("Warehouse Name:");
    if (!name) return;
    const loc = prompt("Location:");

    await fetch(`${API_BASE}/inventory/warehouses`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, location: loc || "Unknown" })
    });
    loadWarehouses();
}

async function handleStockMovement(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        product_id: parseInt(formData.get('product_id')),
        warehouse_id: parseInt(formData.get('warehouse_id')),
        quantity: parseInt(formData.get('quantity')),
        movement_type: formData.get('movement_type') // Query param for router? No, schema body.
    };

    // API expects query params for some, body for others?
    // Inventory Router: 
    // @router.post("/stock") -> add_stock_movement(product_id, warehouse_id, quantity, movement_type)
    // These are Query params by default in FastAPI if not Pydantic model.
    // Let me check my router implementation.
    // def add_stock_movement(product_id: int, ..., movement_type: schemas.MovementType):
    // Yes, these are query parameters!

    const query = new URLSearchParams(data).toString();

    // Wait, movement_type is enum.
    try {
        const res = await fetch(`${API_BASE}/inventory/stock?${query}`, {
            method: "POST"
        });
        if (res.ok) {
            alert("Movement Recorded");
            e.target.reset();
        } else {
            const err = await res.json();
            alert("Error: " + err.detail);
        }
    } catch (e) {
        alert("Error");
    }
}

async function loadStock() {
    const pid = document.getElementById('stock-prod-id').value;
    if (!pid) return;

    const res = await fetch(`${API_BASE}/inventory/stock/${pid}`);
    const stocks = await res.json();

    const tbody = document.getElementById('stock-body');
    tbody.innerHTML = stocks.map(s => `<tr><td>Warehouse ${s.warehouse_id}</td><td>${s.quantity}</td></tr>`).join('');
}

// User: Ordering
async function loadUserProducts() {
    const grid = document.getElementById('user-products-grid');
    if (!grid) return;

    const res = await fetch(`${API_BASE}/products/`);
    const products = await res.json();

    grid.innerHTML = products.map(p => `
        <div class="card">
            <h3 style="margin-top:0;">${p.name}</h3>
            <p style="color:666;">${p.description || "No description"}</p>
            <div style="font-size:1.25rem; font-weight:bold; color:var(--primary-color); margin: 1rem 0;">${formatCurrency(p.unit_price)}</div>
            <div style="display:flex; gap:0.5rem;">
                <input type="number" id="qty-${p.product_id}" value="1" min="1" class="form-input" style="width: 3rem; padding:0.25rem;">
                <button onclick="addToCart(${p.product_id})" class="btn btn-primary" style="flex:1;">Add to Order</button>
            </div>
        </div>
    `).join('');
}

let currentOrderItems = [];

function addToCart(pid) {
    const qty = parseInt(document.getElementById(`qty-${pid}`).value);
    if (qty > 0) {
        const existing = currentOrderItems.find(i => i.product_id === pid);
        if (existing) existing.quantity += qty;
        else currentOrderItems.push({ product_id: pid, quantity: qty });
        updateCartUI();
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) cartCount.textContent = currentOrderItems.reduce((acc, i) => acc + i.quantity, 0);

    const cartList = document.getElementById('cart-items');
    if (cartList) {
        cartList.innerHTML = currentOrderItems.map(i => `<li>Product ${i.product_id} x ${i.quantity}</li>`).join('');
    }
}

async function placeOrder() {
    if (currentOrderItems.length === 0) return alert("Cart empty");

    const customerId = 1; // Simulated hardcoded customer

    // Ensure customer exists? Or create one?
    // We should probably allow the user to create one or input ID.
    // For simplicity, we'll try ID 1. If not exists, we might need to handle it.
    // Better: Helper function to create customer if not exists or input.

    const custIdInput = prompt("Enter Customer ID (default 1):", "1");
    if (!custIdInput) return;

    const orderData = {
        customer_id: parseInt(custIdInput),
        items: currentOrderItems
    };

    try {
        const res = await fetch(`${API_BASE}/orders/`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });

        if (res.ok) {
            alert("Order Placed Successfully!");
            currentOrderItems = [];
            updateCartUI();
        } else {
            const err = await res.json();
            alert("Order Failed: " + err.detail);
        }
    } catch (e) {
        console.error(e);
        alert("Order Failed");
    }
}
