"""Répare les textes UTF-8 importés en latin1 dans le catalogue existant.

À exécuter dans le conteneur backend. Les prix et stocks restent inchangés.
"""

import os

import mysql.connector


def repair_text(value):
    if not any(marker in value for marker in ("Ã", "Â", "â€")):
        return value
    try:
        repaired = value.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return value
    return repaired


def main():
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        charset="utf8mb4",
        autocommit=False,
    )
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id, nom, description, categorie, origine FROM produits FOR UPDATE"
        )
        rows = cursor.fetchall()
        repaired_count = 0
        for product_id, *fields in rows:
            repaired_fields = [repair_text(value) for value in fields]
            if repaired_fields == fields:
                continue
            cursor.execute(
                "UPDATE produits SET nom = %s, description = %s, categorie = %s, "
                "origine = %s WHERE id = %s",
                (*repaired_fields, product_id),
            )
            repaired_count += 1
        connection.commit()
        print(f"Produits corrigés : {repaired_count}")
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
