import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col

# Ajouter le connecteur Cassandra
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages com.datastax.spark:spark-cassandra-connector_2.13:3.5.0 pyspark-shell"

#  Créer la SparkSession avec configuration Cassandra
spark = SparkSession.builder \
    .appName("CassandraProduits") \
    .master("local[*]") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# Lire la table produits du keyspace ecommerce
df_produits = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(keyspace="ecommerce", table="produits") \
    .load()

# Afficher quelques lignes
print("Données existantes dans produits :")
df_produits.show(10)

# Analyse 1 : prix moyen par produit
print("Prix moyen par produit :")
df_produits.groupBy("nom") \
    .agg(avg("prix").alias("prix_moyen")) \
    .orderBy(col("prix_moyen").desc()) \
    .show()

# Analyse 2 : comparaison des prix par vendeur
print("Prix moyen par vendeur :")
df_produits.groupBy("vendeur") \
    .agg(avg("prix").alias("prix_moyen")) \
    .orderBy(col("prix_moyen").desc()) \
    .show()

# Analyse 3 : comparaison des prix par catégorie
print("Prix moyen par catégorie :")
df_produits.groupBy("categorie") \
    .agg(avg("prix").alias("prix_moyen")) \
    .orderBy(col("prix_moyen").desc()) \
    .show()

# Stopper la session Spark
spark.stop()
