# smart-grids-sgbi
Smart Grids: Infraestructura, gestión del dato y BI (SGBI)

## Quick Start

### Install Docker and Docker Compose
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

```bash
sudo apt-get install -y docker-compose
```

### Start the services
```bash
docker-compose up -d
```

### Stop the services
```bash
docker-compose down
```

### Check the logs
```bash
docker-compose logs -f
```

## Kafka
### Access to Kafka container
```bash
docker exec -it kafka bash
```

### Create topic
```bash
kafka-topics.sh --create --topic test --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### Send messages to the topic
```bash
kafka-console-producer.sh --topic test --bootstrap-server localhost:9092
```

## Spark
### Start the Spark container
```bash
docker start spark
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

```sql
SELECT * FROM kafka_messages;
```
