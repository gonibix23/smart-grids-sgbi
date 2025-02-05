from kafka import KafkaConsumer
import json
import psycopg2

# Configuración de Kafka Consumer
consumer = KafkaConsumer(
    'test',  # Nombre del tema
    bootstrap_servers='localhost:9092',  # Cambia 'localhost' si está en otro contenedor
    api_version=(3, 9, 0),
    group_id='test_group',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Configuración de la base de datos TimescaleDB
DB_HOST = "localhost"
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

print("Esperando mensajes... Presiona Ctrl+C para salir.")

try:
    for message in consumer:
        data = message.value
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
    consumer.close()
    cursor.close()
    conn.close()
