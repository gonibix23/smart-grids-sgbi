"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, StructField

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/spark_consumer.py
# command: [ "spark-submit", "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/spark_consumer.py" ]

spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("kafka.api.version", "3.9.0") \
    .option("subscribe", "test") \
    .option("startingOffsets", "earliest") \
    .load()

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("mensaje", StringType(), True)
])

df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
"""

import json
import psycopg2

# Configuración de la base de datos TimescaleDB
DB_HOST = "timescaledb"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kafka_messages (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            data JSONB
        );
    """)
    conn.commit()
except Exception as e:
    print(f"Error conectando a la base de datos: {e}")
    exit(1)

try:
    messages = [
        {
            "value": {"key1": "value1", "key2": "value2"}
        },
        {
            "value": {"key3": "value3", "key4": "value4"}
        },
    ]
    for message in messages:
        data = message["value"]
        print(f"Mensaje recibido: {data}")
        # Insertar datos en TimescaleDB
        try:
            cursor.execute("INSERT INTO kafka_messages (data) VALUES (%s);", [json.dumps(data)])
            conn.commit()
            print("Mensaje insertado en la base de datos.")
        except Exception as db_err:
            print(f"Error insertando en la base de datos: {db_err}")
            conn.rollback()
except KeyboardInterrupt:
    print("Proceso interrumpido por el usuario.")
finally:
    cursor.close()
    conn.close()
