from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, StructField

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/spark_consumer.py
# command: [ "spark-submit", "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/spark_consumer.py" ]

spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("kafka.api.version", "3.9.0") \
    .option("subscribe", "test") \
    .option("startingOffsets", "earliest") \
    .load()

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("mensaje", StringType(), True)
])

df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
