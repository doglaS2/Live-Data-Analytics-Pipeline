from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
        .getOrCreate()

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
        .load()
    
    # convertendo dados pra streaming
    df = df.selectExpr("CAST(value AS STRING)")
    
    # iniciando a query
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    main() 