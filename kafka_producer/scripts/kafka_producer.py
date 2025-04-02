from kafka import KafkaProducer
import json
import logging
import time

# Configura el nivel de log para mostrar mensajes de depuración.
#logging.basicConfig(level=logging.DEBUG)

topic_name = "test"

def connect():
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            api_version=(3, 9, 0),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
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

while (producer := connect()) is None:
    print(f"Topic '{topic_name}' not found or connection failed. Retrying in 5 seconds...")
    time.sleep(5)

print("Successful connection!", producer)

for counter in range(10):
    send_message(topic_name, json.dumps({"producer_key_1": counter}))
