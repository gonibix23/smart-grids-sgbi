FROM python:3.10-slim

WORKDIR /app/scripts

# Copia el archivo de requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta scripts en el contenedor
COPY scripts/ .

# Expone el puerto 5000 si es necesario (por ejemplo, si usas Flask)
EXPOSE 5001

CMD ["python", "kafka_producer.py"]
