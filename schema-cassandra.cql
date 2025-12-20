-- Schema de cassandra

CREATE KEYSPACE IF NOT EXISTS ecommerce
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

-- Utilisation du KEYSPACE
USE ecommerce;

-- TABLE Produits
CREATE TABLE IF NOT EXISTS produits(
    categorie TEXT,
    vendeur TEXT,
    nom TEXT,
    date_collection TIMESTAMP,
    prix DOUBLE,

    PRIMARY KEY(
        (categorie),
        vendeur,
        nom,
        date_collection
    )
);


-- Les index facilitant certains analyses
CREATE INDEX IF NOT EXISTS idx_produits_vendeur
ON produits (vendeur);

CREATE INDEX IF NOT EXISTS idx_produits_nom
ON produits (nom);