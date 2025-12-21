from pyspark.sql import SparkSession

# Création de la session Spark
spark = SparkSession.builder \
    .appName("Analyse E-commerce") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

# Chargement des données depuis Cassandra
df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="produits", keyspace="ecommerce") \
    .load()

# Vérification du schéma et affichage des 5 premières lignes
df.printSchema()
df.show(5)
