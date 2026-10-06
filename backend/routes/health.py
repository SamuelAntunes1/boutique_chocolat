from flask import Blueprint, jsonify
from mysql.connector import Error

from db import query_one

bp = Blueprint("health", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    """Vérifie que Flask et MySQL répondent."""
    try:
        row = query_one("SELECT 1 AS ok")
        return jsonify({
            "status": "ok",
            "backend": True,
            "database": bool(row and row["ok"] == 1),
        })
    except Error as exc:
        return jsonify({
            "status": "degraded",
            "backend": True,
            "database": False,
            "error": str(exc),
        }), 503
