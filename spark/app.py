from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
        .config("spark.sql.shuffle.partitions", "1") \
        .getOrCreate()

def parse_json(df):
    # Define o schema dos dados
    schema = StructType([
        StructField("id", IntegerType()),
        StructField("valor", DoubleType()),
        StructField("timestamp", TimestampType())
    ])
    
    # Converte a string JSON para o schema definido
    return df.select(from_json(col("value"), schema).alias("data")).select("data.*")

def main():
    spark = create_spark_session()
    
    # config do kafka
    kafka_bootstrap_servers = "kafka:9092"
    kafka_topic = "events"
    
    # lendo dados do kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()
    
    # processando os dados
    parsed_df = parse_json(df)
    
    # adicionando timestamp de processamento
    processed_df = parsed_df.withColumn("process_time", current_timestamp())
    
    # iniciando a query
    query = processed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .trigger(processingTime='5 seconds') \
        .start()
    
    # Query para o Druid
    druid_query = processed_df.writeStream \
        .outputMode("append") \
        .format("druid") \
        .option("druid.coordinator.url", "http://druid-coordinator:8081") \
        .option("druid.datasource", "events") \
        .option("druid.ingestion.interval", "PT5S") \
        .trigger(processingTime='5 seconds') \
        .start()
    
    query.awaitTermination()
    druid_query.awaitTermination()

if __name__ == "__main__":
    main() 