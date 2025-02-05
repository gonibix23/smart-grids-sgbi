# smart-grids-sgbi
Smart Grids: Infraestructura, gestión del dato y BI (SGBI)

## Quick Start

### Start the services
```bash
docker-compose up -d
```

### Access to Kafka container
```bash
docker exec -it kafka bash
```

### Execute the scripts for Kafka
```bash
python3 scripts/kafka_producer.py
```

```bash
python3 scripts/kafka_consumer.py
```

### Check TimescaleDB
```bash
docker exec -it timescaledb psql -U myuser -d mydb
```
