import os
import json
import logging
from fastapi import FastAPI, Request
from kafka import KafkaProducer
import uvicorn

# Inicializar FastAPI
app = FastAPI()

# Topic y broker de Kafka
topic_name = "test"
bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Crear el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Ruta para recibir mensajes POST
@app.post("/ingest")
async def ingest_data(request: Request):
    try:
        data = await request.json()
        producer.send(topic_name, data)
        producer.flush()
        logging.info(f"Mensaje recibido y enviado a Kafka: {data}")
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Error al enviar a Kafka: {str(e)}")
        return {"status": "error", "details": str(e)}

# Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
