# smart-grids-sgbi
Smart Grids: Infraestructura, gestión del dato y BI (SGBI)

## Quick Start

### Start the services
```bash
docker-compose up -d
```

## Kafka
### Access to Kafka container
```bash
docker exec -it kafka bash
```

### Execute the scripts to test Kafka
```bash
python3 scripts/kafka_producer.py
```

```bash
python3 scripts/kafka_consumer.py
```

## Spark
### Access to Spark container
```bash
docker exec -it spark bash
```

### Execute the scripts to test Spark Streaming
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/spark_consumer.py
```

## TimescaleDB
### Check the data in TimescaleDB
```bash
docker exec -it timescaledb psql -U myuser -d mydb
```
