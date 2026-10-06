from decimal import Decimal

from flask import Blueprint, jsonify, request, session

from db import get_db, query_all, query_one

bp = Blueprint("commandes", __name__, url_prefix="/api/commandes")


def bad_request(message):
    return jsonify({"error": message}), 400


@bp.post("")
def create_order():
    """Crée une commande et recalcule le total depuis les prix en base."""
    data = request.get_json(silent=True) or {}
    customer = data.get("client") or {}
    items = data.get("articles") or []

    nom = str(customer.get("nom", "")).strip()
    email = str(customer.get("email", "")).strip().lower()
    adresse = str(customer.get("adresse", "")).strip()
    ville = str(customer.get("ville", "")).strip()
    npa = str(customer.get("npa", "")).strip()

    if len(nom) < 2:
        return bad_request("Le nom du client est requis.")
    if "@" not in email:
        return bad_request("L'adresse e-mail est invalide.")
    if not adresse or not ville or not npa:
        return bad_request("L'adresse de livraison est incomplète.")
    if not isinstance(items, list) or not items:
        return bad_request("Le panier est vide.")

    normalized = {}
    for item in items:
        try:
            product_id = int(item.get("produit_id"))
            quantity = int(item.get("quantite"))
        except (TypeError, ValueError, AttributeError):
            return bad_request("Un article du panier est invalide.")

        if product_id <= 0 or quantity <= 0 or quantity > 50:
            return bad_request("Quantité de produit invalide.")
        normalized[product_id] = normalized.get(product_id, 0) + quantity

    placeholders = ",".join(["%s"] * len(normalized))
    products = query_all(
        f"""
        SELECT id, nom, prix, stock
        FROM produits
        WHERE actif = TRUE AND id IN ({placeholders})
        FOR UPDATE
        """,
        tuple(normalized.keys()),
    )

    by_id = {row["id"]: row for row in products}
    if len(by_id) != len(normalized):
        return bad_request("Un ou plusieurs produits n'existent plus.")

    total = Decimal("0.00")
    for product_id, quantity in normalized.items():
        product = by_id[product_id]
        if quantity > product["stock"]:
            return bad_request(
                f"Stock insuffisant pour « {product['nom']} » (disponible : {product['stock']})."
            )
        total += product["prix"] * quantity

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO commandes
                (utilisateur_id, nom_client, email, adresse, npa, ville, total, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'confirmee')
            """,
            (
                session.get("user_id"),
                nom,
                email,
                adresse,
                npa,
                ville,
                total,
            ),
        )
        order_id = cursor.lastrowid

        for product_id, quantity in normalized.items():
            product = by_id[product_id]
            cursor.execute(
                """
                INSERT INTO lignes_commande
                    (commande_id, produit_id, nom_produit, quantite, prix_unitaire)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, product_id, product["nom"], quantity, product["prix"]),
            )
            cursor.execute(
                "UPDATE produits SET stock = stock - %s WHERE id = %s",
                (quantity, product_id),
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()

    return jsonify({
        "id": order_id,
        "statut": "confirmee",
        "total": float(total),
        "message": "Commande enregistrée avec succès.",
    }), 201


@bp.get("/<int:order_id>")
def get_order(order_id):
    order = query_one(
        """
        SELECT id, utilisateur_id, nom_client, email, adresse, npa, ville,
               total, statut, cree_le
        FROM commandes
        WHERE id = %s
        """,
        (order_id,),
    )
    if order is None:
        return jsonify({"error": "Commande introuvable."}), 404

    # Les commandes invitées ne sont pas exposées par une simple URL numérique.
    # Une commande associée à un compte n'est consultable que par son propriétaire.
    if order["utilisateur_id"] is None or order["utilisateur_id"] != session.get("user_id"):
        return jsonify({"error": "Accès refusé."}), 403

    lines = query_all(
        """
        SELECT produit_id, nom_produit, quantite, prix_unitaire
        FROM lignes_commande
        WHERE commande_id = %s
        ORDER BY id
        """,
        (order_id,),
    )

    return jsonify({
        "id": order["id"],
        "client": {
            "nom": order["nom_client"],
            "email": order["email"],
            "adresse": order["adresse"],
            "npa": order["npa"],
            "ville": order["ville"],
        },
        "total": float(order["total"]),
        "statut": order["statut"],
        "cree_le": order["cree_le"].isoformat(),
        "articles": [
            {
                "produit_id": line["produit_id"],
                "nom": line["nom_produit"],
                "quantite": line["quantite"],
                "prix_unitaire": float(line["prix_unitaire"]),
            }
            for line in lines
        ],
    })
