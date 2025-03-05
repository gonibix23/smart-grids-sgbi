# smart-grids-sgbi
Smart Grids: Infraestructura, gestión del dato y BI (SGBI)

## Quick Start

## TODO: Kubernetes Setup
### Check Pods
```bash
kubectl get pods
```

## Kafka
### Check Pods

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


### Create Kafka Producer
```bash
kubectl apply -f ./kafka_producer/kafka-producer.yaml
```

### Delete Kafka Producer
```bash
kubectl delete -f ./kafka_producer/kafka-producer.yaml
```

### Si no se ven con kafka, ejecutar el siguiente comando en otro terminal
```bash
kubectl port-forward svc/kafka 9092:9092
```

## Spark
### Start the Spark container
```bash
docker build -t <usuario de dockerhub>/spark_consumer:latest ./spark_consumer
```

### Push the Spark container
```bash
docker push <usuario de dockerhub>/spark_consumer:latest
```

Hay que cambiar también el nombre de la imagen en el archivo `spark_consumer/spark-consumer.yaml`.

### Create Spark Consumer
```bash
kubectl apply -f ./spark_consumer/spark-consumer.yaml
```

### Delete Spark Consumer
```bash
kubectl delete -f ./spark_consumer/spark-consumer.yaml
```

## TimescaleDB

### Create TimescaleDB
```bash
kubectl apply -f ./timescaledb/timescaledb-cluster.yaml
```

### Delete TimescaleDB
```bash
kubectl delete -f ./timescaledb/timescaledb-cluster.yaml
```

### Check the data in TimescaleDB
```bash
kubectl exec -it timescaledb-xxxx -- bash
```

```bash
psql -U myuser -d mydb
```

```sql
SELECT * FROM kafka_messages;
```

## Grafana TODO: Configurar el servicio de grafana en kubernetes

### Create Grafana
```bash
kubectl apply -f ./grafana/grafana.yaml
```

### Delete Grafana
```bash
kubectl delete -f ./grafana/grafana.yaml
```
