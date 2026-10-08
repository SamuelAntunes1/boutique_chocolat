const API_BASE = "/api";

async function apiRequest(path, options = {}) {
    const config = {
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    };

    const response = await fetch(`${API_BASE}${path}`, config);
    let body = null;

    try {
        body = await response.json();
    } catch (_error) {
        body = null;
    }

    if (!response.ok) {
        throw new Error(body?.error || `Erreur HTTP ${response.status}`);
    }

    return body;
}

function formatPrice(value) {
    return new Intl.NumberFormat("fr-CH", {
        style: "currency",
        currency: "CHF",
    }).format(Number(value));
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = String(value ?? "");
    return div.innerHTML;
}

function getCart() {
    try {
        return JSON.parse(localStorage.getItem("boutique-cart")) || [];
    } catch (_error) {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem("boutique-cart", JSON.stringify(cart));
    updateCartCount();
}

function addToCart(product, quantity = 1) {
    const cart = getCart();
    const existing = cart.find((item) => item.id === product.id);

    if (existing) {
        existing.quantite = Math.min(existing.quantite + quantity, product.stock);
        existing.stock = product.stock;
        existing.prix = product.prix;
    } else {
        cart.push({
            id: product.id,
            nom: product.nom,
            prix: product.prix,
            stock: product.stock,
            cacao: product.cacao,
            categorie: product.categorie,
            quantite: Math.min(quantity, product.stock),
        });
    }

    saveCart(cart);
}

function updateCartCount() {
    const count = getCart().reduce((sum, item) => sum + item.quantite, 0);
    document.querySelectorAll("[data-cart-count]").forEach((element) => {
        element.textContent = count;
    });
}

document.addEventListener("DOMContentLoaded", updateCartCount);
