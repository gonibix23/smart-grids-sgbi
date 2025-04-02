# Usa la imagen oficial de Bitnami Spark como base
FROM bitnami/spark:latest

# Cambiar a usuario root para instalar dependencias
USER root

# Actualizar repositorios e instalar Python y pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Instalar dependencias básicas (si no las tienes en requirements.txt)
RUN pip3 install --no-cache-dir numpy pandas pyspark

# Establecer Python como predeterminado
RUN ln -s /usr/bin/python3 /usr/bin/python

# Definir el directorio de trabajo en Spark
WORKDIR /opt/spark-apps

# Copiar el archivo de requerimientos y los scripts a la imagen
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar los JARs a la ubicación de Spark (suponiendo que la carpeta "jars" está en el mismo nivel que el Dockerfile)
COPY ./jars /opt/spark/jars

# Copiar todos los scripts (incluyendo spark_consumer.py) a /opt/spark-apps
COPY ./scripts/ .

# Configurar el entrypoint para ejecutar spark-submit con el script principal
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "spark_consumer_f.py"]
