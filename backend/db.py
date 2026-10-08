"""Gestion des connexions MySQL pour Flask."""

from flask import current_app, g
import mysql.connector
from mysql.connector import Error


def get_db():
    """Retourne une connexion MySQL ouverte pour la requête courante."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            database=current_app.config["DB_NAME"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            autocommit=False,
        )
    return g.db


def close_db(_error=None):
    """Ferme la connexion MySQL à la fin de la requête."""
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()


def query_all(sql, params=()):
    """Exécute un SELECT et retourne toutes les lignes sous forme de dictionnaires."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close()


def query_one(sql, params=()):
    """Exécute un SELECT et retourne une ligne ou None."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        return cursor.fetchone()
    finally:
        cursor.close()


def init_app(app):
    app.teardown_appcontext(close_db)
