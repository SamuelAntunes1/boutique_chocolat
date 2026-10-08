from flask import Blueprint, jsonify, request, session
from mysql.connector import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, query_one

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def public_user(row):
    return {
        "id": row["id"],
        "nom": row["nom"],
        "email": row["email"],
    }


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    nom = str(data.get("nom", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if len(nom) < 2:
        return jsonify({"error": "Le nom doit contenir au moins 2 caractères."}), 400
    if "@" not in email or len(email) > 190:
        return jsonify({"error": "Adresse e-mail invalide."}), 400
    if len(password) < 6:
        return jsonify({"error": "Le mot de passe doit contenir au moins 6 caractères."}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s)",
            (nom, email, generate_password_hash(password)),
        )
        user_id = cursor.lastrowid
        db.commit()
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Un compte existe déjà avec cette adresse e-mail."}), 409
    finally:
        cursor.close()

    session.clear()
    session["user_id"] = user_id
    return jsonify({"id": user_id, "nom": nom, "email": email}), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    row = query_one(
        "SELECT id, nom, email, mot_de_passe FROM utilisateurs WHERE email = %s",
        (email,),
    )

    if row is None or not check_password_hash(row["mot_de_passe"], password):
        return jsonify({"error": "E-mail ou mot de passe incorrect."}), 401

    session.clear()
    session["user_id"] = row["id"]
    return jsonify(public_user(row))


@bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Déconnexion effectuée."})


@bp.get("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"authenticated": False, "user": None})

    row = query_one(
        "SELECT id, nom, email FROM utilisateurs WHERE id = %s",
        (user_id,),
    )
    if row is None:
        session.clear()
        return jsonify({"authenticated": False, "user": None})

    return jsonify({"authenticated": True, "user": public_user(row)})
