"""Point d'entrée du backend Flask de la boutique de chocolat."""

from flask import Flask, jsonify
from mysql.connector import Error

from config import Config
from db import init_app as init_db
from routes.auth import bp as auth_bp
from routes.commandes import bp as commandes_bp
from routes.health import bp as health_bp
from routes.produits import bp as produits_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(produits_bp)
    app.register_blueprint(commandes_bp)
    app.register_blueprint(auth_bp)

    @app.get("/api")
    def api_index():
        return jsonify({
            "name": "API Boutique Chocolat",
            "version": "1.0",
            "endpoints": [
                "/api/health",
                "/api/produits",
                "/api/produits/<id>",
                "/api/commandes",
                "/api/auth/register",
                "/api/auth/login",
            ],
        })

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Ressource introuvable."}), 404

    @app.errorhandler(Error)
    def database_error(error):
        app.logger.exception("Erreur MySQL")
        return jsonify({"error": "Erreur de base de données.", "detail": str(error)}), 500

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Erreur interne", exc_info=error)
        return jsonify({"error": "Erreur interne du serveur."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
