function cartRow(item) {
    return `
        <article class="cart-row" data-cart-row="${item.id}">
            <div class="mini-chocolate" aria-hidden="true"></div>
            <div class="cart-product">
                <p class="eyebrow">${escapeHtml(item.categorie)} · ${item.cacao}% cacao</p>
                <h3>${escapeHtml(item.nom)}</h3>
                <button class="link-button" data-remove="${item.id}">Retirer</button>
            </div>
            <div class="quantity-control" aria-label="Quantité de ${escapeHtml(item.nom)}">
                <button data-decrease="${item.id}" aria-label="Diminuer">−</button>
                <span>${item.quantite}</span>
                <button data-increase="${item.id}" aria-label="Augmenter">+</button>
            </div>
            <strong class="cart-price">${formatPrice(item.prix * item.quantite)}</strong>
        </article>
    `;
}

function renderCart() {
    const cart = getCart();
    const list = document.getElementById("cart-list");
    const empty = document.getElementById("cart-empty");
    const summary = document.getElementById("cart-summary");

    if (cart.length === 0) {
        list.innerHTML = "";
        empty.hidden = false;
        summary.hidden = true;
        return;
    }

    empty.hidden = true;
    summary.hidden = false;
    list.innerHTML = cart.map(cartRow).join("");

    const total = cart.reduce((sum, item) => sum + Number(item.prix) * item.quantite, 0);
    const quantity = cart.reduce((sum, item) => sum + item.quantite, 0);
    document.getElementById("summary-count").textContent = `${quantity} article${quantity > 1 ? "s" : ""}`;
    document.getElementById("summary-total").textContent = formatPrice(total);

    list.querySelectorAll("[data-decrease]").forEach((button) => {
        button.addEventListener("click", () => changeQuantity(Number(button.dataset.decrease), -1));
    });
    list.querySelectorAll("[data-increase]").forEach((button) => {
        button.addEventListener("click", () => changeQuantity(Number(button.dataset.increase), 1));
    });
    list.querySelectorAll("[data-remove]").forEach((button) => {
        button.addEventListener("click", () => removeItem(Number(button.dataset.remove)));
    });
}

function changeQuantity(id, delta) {
    const cart = getCart();
    const item = cart.find((product) => product.id === id);
    if (!item) return;

    item.quantite = Math.max(1, Math.min(item.quantite + delta, item.stock));
    saveCart(cart);
    renderCart();
}

function removeItem(id) {
    saveCart(getCart().filter((item) => item.id !== id));
    renderCart();
}

document.addEventListener("DOMContentLoaded", renderCart);
