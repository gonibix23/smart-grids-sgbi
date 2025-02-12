from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import logging

# Configura el nivel de log para mostrar mensajes de depuración.
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Se crea un KafkaProducer que se conecta al broker de Kafka.
# Dado que el contenedor producer se encuentra en la misma red que kafka,
# usamos 'kafka:9092' como bootstrap_servers.
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    api_version=(3, 9, 0),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/send', methods=['POST'])
def send_message():
    """
    Endpoint que recibe una petición POST con un JSON que debe incluir:
      - "topic": nombre del topic de Kafka
      - "message": mensaje a enviar (puede ser string o estructura serializable)
    """
    data = request.get_json()
    if not data or 'topic' not in data or 'message' not in data:
        return jsonify({'error': 'El payload debe incluir "topic" y "message".'}), 400

    topic = data['topic']
    message = data['message']
    try:
        # Envia el mensaje al topic indicado
        producer.send(topic, message)
        # Se asegura de enviar el mensaje
        producer.flush()
        logging.info(f'Mensaje enviado al topic {topic}')
        return jsonify({'status': f'Mensaje enviado al topic {topic}'}), 200
    except Exception as e:
        logging.error(f'Error al enviar mensaje al topic {topic}: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ejecuta el servidor en todas las interfaces de red para permitir acceso externo.
    app.run(host='0.0.0.0', port=5000)
