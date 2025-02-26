from pyspark.sql import SparkSession # type: ignore

# Iniciar la sesión de Spark
spark = SparkSession.builder \
    .appName("SparkTimescale") \
    .config("spark.jars", "C:/Users/v-er-/Downloads/postgresql-42.7.5.jar") \
    .getOrCreate()

# Leer los datos desde TimescaleDB
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://timescaledb:5432/mydb") \
    .option("dbtable", "dbproyecto") \
    .option("user", "admin") \
    .option("password", "password") \
    .load()

# Mostrar los datos
df.show()
