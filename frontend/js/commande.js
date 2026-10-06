function renderOrderSummary() {
    const cart = getCart();
    const container = document.getElementById("order-items");
    const submit = document.getElementById("submit-order");

    if (cart.length === 0) {
        container.innerHTML = '<p class="muted">Ton panier est vide.</p>';
        document.getElementById("order-total").textContent = formatPrice(0);
        submit.disabled = true;
        return;
    }

    container.innerHTML = cart.map((item) => `
        <div class="order-line">
            <span>${item.quantite} × ${escapeHtml(item.nom)}</span>
            <strong>${formatPrice(item.quantite * item.prix)}</strong>
        </div>
    `).join("");

    const total = cart.reduce((sum, item) => sum + item.quantite * Number(item.prix), 0);
    document.getElementById("order-total").textContent = formatPrice(total);
}

async function submitOrder(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const button = document.getElementById("submit-order");
    const message = document.getElementById("order-message");
    const cart = getCart();

    if (cart.length === 0) {
        message.className = "notice notice-error";
        message.textContent = "Le panier est vide.";
        return;
    }

    if (!form.reportValidity()) return;

    const formData = new FormData(form);
    const payload = {
        client: {
            nom: formData.get("nom"),
            email: formData.get("email"),
            adresse: formData.get("adresse"),
            npa: formData.get("npa"),
            ville: formData.get("ville"),
        },
        articles: cart.map((item) => ({
            produit_id: item.id,
            quantite: item.quantite,
        })),
    };

    button.disabled = true;
    button.textContent = "Enregistrement…";
    message.hidden = true;

    try {
        const result = await apiRequest("/commandes", {
            method: "POST",
            body: JSON.stringify(payload),
        });

        saveCart([]);
        form.hidden = true;
        document.getElementById("order-summary-card").hidden = true;
        const confirmation = document.getElementById("order-confirmation");
        confirmation.hidden = false;
        confirmation.innerHTML = `
            <p class="eyebrow">Commande confirmée</p>
            <h2>Merci pour ta commande.</h2>
            <p>La commande <strong>#${result.id}</strong> a été enregistrée pour un montant de <strong>${formatPrice(result.total)}</strong>.</p>
            <a class="button" href="index.html">Retour au catalogue</a>
        `;
    } catch (error) {
        message.hidden = false;
        message.className = "notice notice-error";
        message.textContent = error.message;
        button.disabled = false;
        button.textContent = "Confirmer la commande";
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    renderOrderSummary();
    document.getElementById("checkout-form").addEventListener("submit", submitOrder);

    // Préremplissage facultatif si l'utilisateur s'est authentifié via l'API.
    try {
        const auth = await apiRequest("/auth/me");
        if (auth.authenticated) {
            document.getElementById("nom").value = auth.user.nom;
            document.getElementById("email").value = auth.user.email;
        }
    } catch (_error) {
        // La commande invité reste disponible même si cette requête échoue.
    }
});
