# Utiliza una imagen base de Python ligera
FROM python:3.10.12

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Define el comando de inicio, en este caso, ejecutar el script producer.py
CMD ["python", "kafka_producer.py"]
