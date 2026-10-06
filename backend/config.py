"""Configuration de l'application Flask.

Toutes les valeurs sensibles sont lues depuis les variables d'environnement.
Le fichier .env est chargé par Docker Compose, pas directement par Flask.
"""

import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "boutique")
    DB_USER = os.getenv("DB_USER", "boutique_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    JSON_SORT_KEYS = False
