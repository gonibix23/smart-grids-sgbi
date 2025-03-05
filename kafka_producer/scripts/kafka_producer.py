import os
import json
import logging
import time
from kafka import KafkaProducer

# Configura el nivel de log para mostrar mensajes de depuración.
#logging.basicConfig(level=logging.DEBUG)

topic_name = "test"

# Obtén la dirección del broker desde la variable de entorno o usa localhost por defecto.
bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def connect():
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(3, 9, 0),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logging.info("Connected to Kafka successfully at %s.", bootstrap_servers)
    except Exception as error:
        print("Error connecting to Kafka:", error)

    return producer

def send_message(topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        print(f'Mensaje enviado al topic {topic}')
    except Exception as e:
        print(f'Error al enviar mensaje al topic {topic}: {str(e)}')

# Intenta conectarse a Kafka hasta lograrlo.
while (producer := connect()) is None:
    logging.warning("Connection failed. Retrying in 5 seconds...")
    time.sleep(5)

logging.info("Successful connection! Producer: %s", producer)

# Envía mensajes de forma continua.
while True:
    time.sleep(1)
    send_message(topic_name, {"producer_key_1": time.time()})
