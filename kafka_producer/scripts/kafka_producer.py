from kafka import KafkaProducer
import json
import logging
import time

# Configura el nivel de log para mostrar mensajes de depuración.
logging.basicConfig(level=logging.DEBUG)

topic_name = "test"

def connect():
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            api_version=(3, 9, 0),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logging.info("Connected to Kafka successfully.")
    except Exception as error:
        logging.error("Error connecting to Kafka: %s", error)

    return producer

def send_message(topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        logging.info('Message sent to topic %s', topic)
    except Exception as e:
        logging.error('Error sending message to topic %s: %s', topic, str(e))

while (producer := connect()) is None:
    logging.warning("Topic '%s' not found or connection failed. Retrying in 5 seconds...", topic_name)
    time.sleep(5)

logging.info("Successful connection! %s", producer)

while True:
    time.sleep(1)
    send_message(topic_name, json.dumps({"producer_key_1": time.time()}))

