from pyspark.sql import SparkSession
from pyspark.sql.utils import StreamingQueryException
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, StructField

import json
import psycopg2
import time

DB_HOST = "timescaledb"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

kafka_broker = "kafka:9092"
topic_name = "test"

def start_streaming_job():
    try:
        df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_broker) \
            .option("subscribe", topic_name) \
            .option("startingOffsets", "earliest") \
            .load()

        df_messages = df.selectExpr("CAST(value AS STRING)")

        def insert_into_database(row):
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT
                )
                cursor = conn.cursor()
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
            
            print(f"Mensaje recibido: {row.value}")
            try:
                cursor.execute("INSERT INTO kafka_messages (data) VALUES (%s);", [row.value])
                conn.commit()
                print("Mensaje insertado en la base de datos.")
            except Exception as db_err:
                print(f"Error insertando en la base de datos: {db_err}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

        query = df_messages.writeStream \
            .foreach(insert_into_database) \
            .start()

        query.awaitTermination()
    except StreamingQueryException as e:
        print(f"Error: {e}.")
        return False
    except Exception as e:
        print(f"General error: {e}.")
        return False
    
    return True

while not start_streaming_job():
    print(f"Topic '{topic_name}' not found or connection failed. Retrying in 5 seconds...")
    time.sleep(5)
