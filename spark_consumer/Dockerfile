# Usa la imagen oficial de Bitnami Spark como base
FROM bitnami/spark:latest

# Instalar Python y paquetes necesarios
USER root

RUN mkdir -p /var/lib/apt/lists/partial

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN pip3 install --no-cache-dir numpy pandas pyspark

# Establecer Python como predeterminado
RUN ln -s /usr/bin/python3 /usr/bin/python

# Definir el directorio de trabajo en Spark
WORKDIR /opt/spark-apps

# Copiar los scripts de Python (opcional, si los tienes)
COPY ./scripts /opt/spark-apps

# Definir el entrypoint (para que se pueda ejecutar código de Python dentro de Spark)
CMD ["/bin/bash"]