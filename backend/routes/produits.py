from flask import Blueprint, jsonify, request

from db import query_all, query_one

bp = Blueprint("produits", __name__, url_prefix="/api/produits")


def serialize_product(row):
    return {
        "id": row["id"],
        "nom": row["nom"],
        "description": row["description"],
        "categorie": row["categorie"],
        "origine": row["origine"],
        "cacao": row["cacao"],
        "prix": float(row["prix"]),
        "stock": row["stock"],
    }


@bp.get("")
def list_products():
    """Liste le catalogue avec recherche et filtre de catégorie facultatifs."""
    search = request.args.get("q", "").strip()
    categorie = request.args.get("categorie", "").strip()

    sql = """
        SELECT id, nom, description, categorie, origine, cacao, prix, stock
        FROM produits
        WHERE actif = TRUE
    """
    params = []

    if search:
        sql += " AND (nom LIKE %s OR description LIKE %s OR origine LIKE %s)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if categorie:
        sql += " AND categorie = %s"
        params.append(categorie)

    sql += " ORDER BY nom"
    rows = query_all(sql, tuple(params))
    return jsonify([serialize_product(row) for row in rows])


@bp.get("/<int:product_id>")
def get_product(product_id):
    row = query_one(
        """
        SELECT id, nom, description, categorie, origine, cacao, prix, stock
        FROM produits
        WHERE id = %s AND actif = TRUE
        """,
        (product_id,),
    )

    if row is None:
        return jsonify({"error": "Produit introuvable."}), 404

    return jsonify(serialize_product(row))


@bp.get("/categories")
def list_categories():
    rows = query_all(
        "SELECT DISTINCT categorie FROM produits WHERE actif = TRUE ORDER BY categorie"
    )
    return jsonify([row["categorie"] for row in rows])
