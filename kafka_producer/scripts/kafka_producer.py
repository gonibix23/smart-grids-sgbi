from kafka import KafkaProducer
import json

# Configuración del productor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(3, 9, 0),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Función principal
def main():
    topic = 'test'  # Nombre del tema en Kafka
    print("Introduce los mensajes que deseas enviar. Escribe 'salir' para terminar.")

    while True:
        message = input("Mensaje: ")
        if message.lower() == 'salir':
            break
        producer.send(topic, value={'message': message})
        print(f"Mensaje enviado: {message}")

    producer.flush()
    producer.close()

if __name__ == "__main__":
    main()
