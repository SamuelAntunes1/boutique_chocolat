# Maison Cacao — Boutique de démonstration

Projet réalisé pour le module I347. L'application correspond à une stack web composée d'un frontend statique, d'une API Flask et d'une base MySQL.

## Fonctionnalités applicatives

- catalogue chargé depuis MySQL ;
- recherche et filtre par catégorie ;
- page de détail d'un produit ;
- panier persistant dans le `localStorage` du navigateur ;
- contrôle des quantités selon le stock ;
- création de commande via l'API ;
- recalcul du montant côté serveur ;
- diminution du stock lors d'une commande ;
- inscription, connexion et déconnexion via session Flask ;
- endpoint de santé pour vérifier le backend et MySQL.

## Arborescence

```text
backend/
  app.py
  config.py
  db.py
  routes/
    auth.py
    commandes.py
    health.py
    produits.py
frontend/
  html/
  css/
  js/
db/
  init.sql
nginx/
  Dockerfile
  default.conf
backend/Dockerfile
docker-compose.yml
```

## API

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/health` | État du backend et de MySQL |
| GET | `/api/produits` | Liste des produits |
| GET | `/api/produits/<id>` | Détail d'un produit |
| GET | `/api/produits/categories` | Catégories disponibles |
| POST | `/api/commandes` | Création d'une commande |
| GET | `/api/commandes/<id>` | Consultation d'une commande |
| POST | `/api/auth/register` | Création d'un compte |
| POST | `/api/auth/login` | Connexion |
| POST | `/api/auth/logout` | Déconnexion |
| GET | `/api/auth/me` | Session en cours |

## Charger les produits de démonstration

Le fichier `db/init.sql` contient 14 produits de démonstration, avec des prix et des stocks fictifs. Ils sont chargés automatiquement lors de la première création de la base MySQL.

Si le volume MySQL existe déjà, un redémarrage ne recharge pas ce fichier. Une fois le service `db` démarré, exécuter cette commande depuis la racine du projet dans PowerShell :

```powershell
Get-Content -Raw -Encoding utf8 db/init.sql | docker compose exec -T db sh -c 'exec mysql --default-character-set=utf8mb4 -uroot -p"$MYSQL_ROOT_PASSWORD"'
```

Le script ajoute uniquement les produits dont le nom est absent. Il conserve les produits existants, leurs stocks et les commandes. Recharger ensuite la page du catalogue pour voir les nouveaux produits.

Si une ancienne importation a transformé les accents en caractères comme `Ã©`, réparer les textes existants avant de recharger `init.sql` :

```powershell
docker compose cp db/repair_product_encoding.py backend:/tmp/repair_product_encoding.py
docker compose exec -T backend python /tmp/repair_product_encoding.py
```

Cette correction conserve les identifiants, prix et stocks. Le fichier `init.sql` définit maintenant explicitement l'encodage UTF-8 du client MySQL pour les prochaines initialisations.

## Variables d'environnement du backend

Le backend attend les variables suivantes :

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
SECRET_KEY
```

Un exemple existe dans `.env.exemple`. Les secrets réels ne doivent pas être versionnés.

## Tester le site en local

Le catalogue vient de l'API Flask et de MySQL. Ouvrir directement `frontend/html/index.html`, ou le servir avec un simple serveur statique, ne lance pas l'API et ne permet pas de tester la boutique complète.

1. Démarrer Docker Desktop avec les conteneurs Linux.
2. Si `.env` est absent, copier `.env.exemple` vers `.env`. Renseigner `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `DB_PASSWORD` et `SECRET_KEY`. Pour un lancement hors Docker, `DB_PASSWORD` doit correspondre à `MYSQL_PASSWORD` ; Docker Compose utilise directement `MYSQL_PASSWORD` pour le backend.
3. Dans PowerShell, depuis la racine du projet, lancer :

```powershell
docker compose up -d --build
docker compose ps
```

Compose attend que MySQL et l'API soient prêts avant de démarrer Nginx. Le premier lancement peut prendre quelques minutes pour télécharger les images et initialiser MySQL.

Ouvrir ensuite **http://localhost/** dans le navigateur. Nginx sert les pages, les CSS et les scripts, et transmet les requêtes `/api` à Flask. Le backend utilise le service `db` sur le réseau Docker, même si le `.env` local définit une autre adresse MySQL.

Pour vérifier le fonctionnement :

- **http://localhost/api/health** doit afficher `status: "ok"` et `database: true` ;
- **http://localhost/api/produits** doit afficher la liste des produits en JSON ;
- sur la boutique, vérifier la recherche, les catégories, une fiche produit, l'ajout au panier et une commande avec des coordonnées fictives. La commande doit diminuer le stock des produits achetés.

Si la base existait avant l'ajout des six nouveaux produits, appliquer la commande de la section « Charger les produits de démonstration ».

En cas de problème, consulter :

```powershell
docker compose logs --tail=100 db backend nginx
```

Si le port 80 est déjà utilisé, remplacer `"80:80"` par `"8080:80"` dans `docker-compose.yml`, relancer la stack et ouvrir **http://localhost:8080/**.

Après une modification du frontend ou du backend, relancer `docker compose up -d --build`. Pour arrêter les services en conservant les données :

```powershell
docker compose down
```
