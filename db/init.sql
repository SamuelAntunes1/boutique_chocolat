-- Le client MySQL doit lire les textes du fichier en UTF-8.
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS boutique
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE boutique;

CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS produits (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    origine VARCHAR(80) NOT NULL,
    cacao TINYINT UNSIGNED NOT NULL,
    prix DECIMAL(8,2) NOT NULL,
    stock INT UNSIGNED NOT NULL DEFAULT 0,
    actif BOOLEAN NOT NULL DEFAULT TRUE,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_cacao CHECK (cacao BETWEEN 0 AND 100),
    CONSTRAINT chk_prix CHECK (prix >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS commandes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT UNSIGNED NULL,
    nom_client VARCHAR(100) NOT NULL,
    email VARCHAR(190) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    npa VARCHAR(20) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    statut ENUM('confirmee', 'preparee', 'expediee', 'annulee') NOT NULL DEFAULT 'confirmee',
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_commandes_utilisateur
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
        ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS lignes_commande (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    commande_id INT UNSIGNED NOT NULL,
    produit_id INT UNSIGNED NULL,
    nom_produit VARCHAR(120) NOT NULL,
    quantite INT UNSIGNED NOT NULL,
    prix_unitaire DECIMAL(8,2) NOT NULL,
    CONSTRAINT fk_lignes_commande
        FOREIGN KEY (commande_id) REFERENCES commandes(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_lignes_produit
        FOREIGN KEY (produit_id) REFERENCES produits(id)
        ON DELETE SET NULL,
    CONSTRAINT chk_quantite CHECK (quantite > 0)
) ENGINE=InnoDB;

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Noir Intense 72%',
       'Tablette puissante aux notes de fruits rouges et de café, avec une finale longue et peu sucrée.',
       'Noir', 'Équateur', 72, 8.90, 24
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Noir Intense 72%');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Noir Grand Cru 85%',
       'Un chocolat noir profond, boisé et légèrement épicé pour les amateurs de cacao corsé.',
       'Noir', 'Pérou', 85, 9.80, 18
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Noir Grand Cru 85%');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Lait Caramel Fleur de Sel',
       'Chocolat au lait fondant, caramel croustillant et pointe de fleur de sel.',
       'Lait', 'Suisse', 42, 8.50, 30
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Lait Caramel Fleur de Sel');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Lait Noisettes Grillées',
       'Tablette généreuse au chocolat au lait et noisettes entières délicatement torréfiées.',
       'Lait', 'Suisse', 38, 9.20, 26
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Lait Noisettes Grillées');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Blanc Vanille Bourbon',
       'Chocolat blanc onctueux relevé par une vanille Bourbon naturelle et aromatique.',
       'Blanc', 'Madagascar', 32, 8.40, 20
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Blanc Vanille Bourbon');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Praliné Amandes',
       'Praliné fondant aux amandes torréfiées, enrobé d’un chocolat au lait équilibré.',
       'Praliné', 'Suisse', 40, 11.90, 16
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Praliné Amandes');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Noir Orange Confite',
       'Alliance d’un chocolat noir fruité et de fines écorces d’orange confite.',
       'Noir', 'République dominicaine', 67, 9.40, 22
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Noir Orange Confite');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Dégustation 6 Carrés',
       'Assortiment de six grands carrés pour découvrir plusieurs intensités de cacao.',
       'Assortiment', 'Sélection', 70, 14.90, 14
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Dégustation 6 Carrés');

-- Produits de démonstration supplémentaires : prix et stocks fictifs.
INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Noir Framboise 70%',
       'Chocolat noir aux éclats de framboise, avec une touche acidulée et une texture croquante.',
       'Noir', 'Équateur', 70, 9.60, 20
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Noir Framboise 70%');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Noir Café 75%',
       'Tablette de chocolat noir aux éclats de café torréfié, pour une dégustation intense et aromatique.',
       'Noir', 'Pérou', 75, 9.90, 18
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Noir Café 75%');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Lait Amandes Croquantes',
       'Chocolat au lait crémeux garni d’amandes grillées pour une pause douce et croquante.',
       'Lait', 'Suisse', 40, 9.30, 24
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Lait Amandes Croquantes');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Lait Spéculoos',
       'Chocolat au lait fondant et brisures de spéculoos aux délicates notes de cannelle.',
       'Lait', 'Suisse', 38, 8.90, 28
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Lait Spéculoos');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Blanc Citron',
       'Chocolat blanc onctueux aux éclats de citron, pour une dégustation fraîche et acidulée.',
       'Blanc', 'Suisse', 30, 8.70, 20
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Blanc Citron');

INSERT INTO produits (nom, description, categorie, origine, cacao, prix, stock)
SELECT 'Praliné Noisettes',
       'Praliné aux noisettes torréfiées enrobé de chocolat au lait, au cœur fondant et généreux.',
       'Praliné', 'Suisse', 40, 12.50, 16
WHERE NOT EXISTS (SELECT 1 FROM produits WHERE nom = 'Praliné Noisettes');
