# smart-grids-sgbi
Smart Grids: Infraestructura, gestión del dato y BI (SGBI)

## Quick Start

## TODO: Kubernetes Setup
### Check Pods
```bash
kubectl get pods
```

## Docker Setup

### Create Pass for Docker

https://docs.docker.com/desktop/setup/sign-in/

### Login to Docker
```bash
docker login
```

## Full Deployment
```bash
kubectl apply -f full_deployment.yaml
```

## Delete Full Deployment
```bash
kubectl delete -f full_deployment.yaml
```

## Kafka Producer
### Build Kafka Producer container
```bash
docker build -t <usuario de dockerhub>/kafka_producer:latest ./kafka_producer
```

### Push Kafka Producer container
```bash
docker push <usuario de dockerhub>/kafka_producer:latest
```

Hay que cambiar también el nombre de la imagen en el archivo `kafka_producer/kafka-producer.yaml`.

### Si no se ven con kafka, ejecutar el siguiente comando en otro terminal
```bash
kubectl port-forward svc/kafka 9092:9092
```

## Spark Consumer
### Build Spark Consumer container
```bash
docker build -t <usuario de dockerhub>/spark_consumer:latest ./spark_consumer
```

### Push the Spark container
```bash
docker push <usuario de dockerhub>/spark_consumer:latest
```

Hay que cambiar también el nombre de la imagen en el archivo `spark_consumer/spark-consumer.yaml`.

### Check the data in TimescaleDB
```bash
kubectl exec -it timescaledb-xxxx -- bash
```

```bash
psql -U myuser -d mydb
```

### Check databases in TimescaleDB
```sql
\l
```

### Select the database
```sql
\c mydb
```

### Check tables in TimescaleDB
```sql
\dt
```

```sql
SELECT * FROM kafka_messages;
```

## Grafana
### Access Grafana
```bash
localhost:32000
```
