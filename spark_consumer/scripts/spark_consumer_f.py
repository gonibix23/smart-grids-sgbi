import os
import json
import time
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.utils import StreamingQueryException

# Datos de conexión a la base de datos TimescaleDB
DB_HOST = "timescaledb"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

# Configura la sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

# Obtén el broker de Kafka desde una variable de entorno; por defecto usa localhost:9092
kafka_broker = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
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

        # Función para crear la tabla y la hipertabla
        def create_table_and_hypertable():
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
                    CREATE TABLE IF NOT EXISTS consumos (
                        id SERIAL,
                        id_casa TEXT,
                        consumo_kwh FLOAT,
                        temperatura FLOAT,
                        irradiacion_solar FLOAT,
                        placas BOOLEAN,
                        produccion_solar_kwh FLOAT,
                        ts TIMESTAMPTZ DEFAULT NOW(),
                        PRIMARY KEY (ts, ID)
                    );
                """)
                conn.commit()
                cursor.execute("SELECT create_hypertable('consumos', 'ts', if_not_exists => TRUE);")
                conn.commit()
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error conectando a la base de datos: {e}")
                if 'conn' in locals():
                    if conn:
                        conn.rollback()
                        if 'cursor' in locals():
                            cursor.close()
                        conn.close()
                return False
            return True

        if not create_table_and_hypertable():
            return False

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

            except Exception as e:
                print(f"Error connecting to database: {e}")
                if 'conn' in locals():
                    if conn:
                        conn.rollback()
                        if 'cursor' in locals():
                            cursor.close()
                        conn.close()
                return

            print(f"Message received 2: {row.value}")
            try:
                data = json.loads(row.value)
                cursor.execute("""
                    INSERT INTO consumos (id_casa, consumo_kwh, temperatura, irradiacion_solar, placas, produccion_solar_kwh)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """, (
                    data['id_casa'],
                    data['consumo_kwh'],
                    data['temperatura'],
                    data['irradiacion_solar'],
                    data['placas'],
                    data['produccion_solar_kwh']
                ))
                conn.commit()
                print("Message inserted into database.")
            except Exception as db_err:
                print(f"Error inserting into database: {db_err}")
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

while True:
    if start_streaming_job():
        print("Streaming job finished or stopped, restarting.")
    else:
        print(f"Topic '{topic_name}' not found or connection failed. Retrying in 5 seconds...")
        time.sleep(5)
