# Projet Web Scraping E-commerce

Ce projet implémente un pipeline complet de données, allant du scraping de sites e-commerce à l'analyse des données avec Spark, en passant par un nettoyage ETL et un stockage dans Cassandra.

## Table des Matières

1.  [Prérequis](#prérequis)
2.  [Installation](#installation)
3.  [Utilisation du Pipeline](#utilisation-du-pipeline)
    *   [1. Scraping des Données](#1-scraping-des-données)
    *   [2. Nettoyage des Données (ETL)](#2-nettoyage-des-données-etl)
    *   [3. Lancement de l'Infrastructure](#3-lancement-de-linfrastructure)
    *   [4. Configuration de la Base de Données (Cassandra)](#4-configuration-de-la-base-de-données-cassandra)
    *   [5. Analyse des Données (Spark)](#5-analyse-des-données-spark)
4.  [Structure du Projet](#-structure-du-projet)
5.  [Auteurs / Contexte Académique](#-auteurs--contexte-académique)


## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

*   **Python 3.11** : Pour les scripts de scraping et d'analyse Spark.
*   **Docker & Docker Compose** : Pour lancer l'infrastructure (Cassandra).
*   **Pentaho Data Integration (PDI)** : Pour exécuter les jobs ETL de nettoyage.
*   **Java (JDK 17 recommandé)** : Nécessaire pour exécuter Spark et Pentaho.

## Installation

1.  Clonez ce dépôt :
    ```bash
    git clone <votre-repo-url>
    cd web-scraping-ecommerce
    ```
2.  Créez un environnement virtuel Python :
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # Sur Linux/Mac
    .\venv\Scripts\activate  # Sur Windows
    ```

3.  Installez les dépendances Python :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation du Pipeline

Suivez ces étapes dans l'ordre pour exécuter le projet de bout en bout.

### 1. Scraping des Données

Lancez le script Python pour récupérer les données des sites e-commerce configurés (Manojia, Jumia, Expat-Dakar).

```bash
python script_scraping.py
```

*   **Résultat** : Un fichier brut est généré dans `data/produits.csv`.

### 2. Nettoyage des Données (ETL)

Utilisez **Pentaho Data Integration** pour nettoyer et transformer les données brutes.

1.  Ouvrez Pentaho (Spoon).
2.  Ouvrez le fichier `job_etl.kjb` (ou la transformation `Transformation 1.ktr` si vous souhaitez exécuter uniquement la transformation).
3.  Exécutez le job.

*   **Résultat** : Un fichier propre est généré dans `output/produits_clean.csv`.

### 3. Lancement de l'Infrastructure

Démarrez le conteneur Cassandra à l'aide de Docker Compose.

```bash
docker-compose up -d
```

Attendez quelques secondes que le conteneur soit complètement opérationnel.

### 4. Configuration de la Base de Données (Cassandra)

Une fois Cassandra lancé, vous devez créer le schéma (Keyspace et Table) et importer les données nettoyées.

Exécutez la commande suivante pour appliquer le script `schema.cql` à l'intérieur du conteneur :

```bash
docker exec -it cassandra-lab cqlsh -f /schema.cql
```

*   **Action** : Cette commande crée le keyspace `ecommerce`, la table `produits`, et importe les données depuis `/data/produits_clean.csv` (monté via Docker).

### 5. Analyse des Données (Spark)

Enfin, lancez le script Spark pour effectuer des analyses sur les données stockées dans Cassandra.

```bash
python spark.py
```

Le script affichera dans la console :
*   Un aperçu des données.
*   Le prix moyen par vendeur.
*   Le prix moyen par catégorie.
*   Le nombre de produits par catégorie.

---

## Structure du Projet

*   `script_scraping.py` : Script de collecte de données.
*   `data/` : Dossier contenant les données brutes (`produits.csv`).
*   `Transformation 1.ktr` / `job_etl.kjb` : Fichiers ETL Pentaho.
*   `output/` : Dossier contenant les données nettoyées (`produits_clean.csv`).
*   `docker-compose.yml` : Configuration Docker pour Cassandra.
*   `schema.cql` : Script CQL pour la structure de la base de données et l'import.
*   `spark.py` : Script d'analyse PySpark connecté à Cassandra.

---

## Auteurs / Contexte Académique

Ce projet a été réalisé dans le cadre d'un cursus universitaire. Il vise à démontrer la mise en œuvre d'une architecture Big Data complète pour l'ingestion, le traitement et l'analyse de données.

**Développeur :**
*   El Hadji Abdou DRAME - Étudiant en Master 2 Informatique Specialite Génie Logiciel à l'Université Assane Seck de Ziguinchor
* Email : [elabdoudrame2001@gmail.com](mailto:elabdoudrame2001@gmail.com)
* LinkedIn : [Profile LinkedIn](https://www.linkedin.com/in/elhadji-abdou-drame/)
* GitHub : [Profile GitHub](https://github.com/eadarak00)
* Portfolio : [Profile LinkedIn](https://eadarak-dev.netlify.app/)

**Encadreur :**
*   Mme. Marie DIOP NDIAYE - Professeure d'Informatique à l'Université Assane Seck de Ziguinchor

**Objectifs Pédagogiques :**
*   Maîtriser le scraping de données web.
*   Mettre en place des pipelines ETL avec Pentaho.
*   Administrer une base de données NoSQL (Cassandra) via Docker.
*   Effectuer des traitements distribués avec Apache Spark.
