let allProducts = [];

function productCard(product) {
    const stockLabel = product.stock > 0 ? `${product.stock} en stock` : "Épuisé";
    return `
        <article class="product-card">
            <a class="product-visual" href="produit.html?id=${product.id}" aria-label="Voir ${escapeHtml(product.nom)}">
                <span class="cacao-badge">${product.cacao}% cacao</span>
                <span class="chocolate-piece" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
            </a>
            <div class="product-body">
                <p class="eyebrow">${escapeHtml(product.categorie)} · ${escapeHtml(product.origine)}</p>
                <h3><a href="produit.html?id=${product.id}">${escapeHtml(product.nom)}</a></h3>
                <p class="product-description">${escapeHtml(product.description)}</p>
                <div class="product-footer">
                    <div>
                        <strong>${formatPrice(product.prix)}</strong>
                        <small>${stockLabel}</small>
                    </div>
                    <button class="button button-small" data-add-product="${product.id}" ${product.stock < 1 ? "disabled" : ""}>
                        Ajouter
                    </button>
                </div>
            </div>
        </article>
    `;
}

function renderProducts(products) {
    const grid = document.getElementById("product-grid");
    const empty = document.getElementById("catalogue-empty");
    grid.innerHTML = products.map(productCard).join("");
    empty.hidden = products.length !== 0;

    document.querySelectorAll("[data-add-product]").forEach((button) => {
        button.addEventListener("click", () => {
            const product = allProducts.find((item) => item.id === Number(button.dataset.addProduct));
            if (!product) return;
            addToCart(product, 1);
            button.textContent = "Ajouté";
            setTimeout(() => (button.textContent = "Ajouter"), 900);
        });
    });
}

function applyFilters() {
    const query = document.getElementById("search").value.trim().toLowerCase();
    const category = document.getElementById("category").value;

    const filtered = allProducts.filter((product) => {
        const matchesQuery = !query || [product.nom, product.description, product.origine]
            .join(" ")
            .toLowerCase()
            .includes(query);
        const matchesCategory = !category || product.categorie === category;
        return matchesQuery && matchesCategory;
    });

    renderProducts(filtered);
}

async function loadCatalogue() {
    const grid = document.getElementById("product-grid");
    try {
        allProducts = await apiRequest("/produits");
        const categories = [...new Set(allProducts.map((product) => product.categorie))].sort();
        const select = document.getElementById("category");
        select.innerHTML = '<option value="">Toutes les catégories</option>' + categories
            .map((category) => `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`)
            .join("");
        renderProducts(allProducts);
    } catch (error) {
        grid.innerHTML = `<div class="notice notice-error">Impossible de charger le catalogue : ${escapeHtml(error.message)}</div>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("search").addEventListener("input", applyFilters);
    document.getElementById("category").addEventListener("change", applyFilters);
    loadCatalogue();
});
