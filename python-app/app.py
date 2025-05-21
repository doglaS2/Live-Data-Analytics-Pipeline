from kafka import KafkaProducer, KafkaConsumer
import json
import time
import threading
import random
from kafka.errors import NoBrokersAvailable
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, TimestampType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verificar_topic_kafka():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        topics = consumer.topics()
        logger.info(f"Tópicos disponíveis: {topics}")
        consumer.close()
        return 'events' in topics
    except Exception as e:
        logger.error(f"Erro ao verificar tópicos: {e}")
        return False

def esperar_kafka(max_retries=30, retry_interval=1):
    for i in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=['kafka:9092'],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            producer.close()
            logger.info("Kafka está pronto!")
            
            # ver se o tópico existe
            if verificar_topic_kafka():
                logger.info("Tópico 'events' encontrado!")
                return True
            else:
                logger.warning("Tópico 'events' não encontrado!")
                return False
                
        except NoBrokersAvailable:
            logger.info(f"Kafka ainda não está pronto. Tentativa {i+1}/{max_retries}")
            time.sleep(retry_interval)
    return False

def iniciar_spark():
    logger.info("Iniciando Spark...")
    spark = SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
        .getOrCreate()
    
    # definir o schema para os eventos
    schema = StructType([
        StructField("id", IntegerType()),
        StructField("valor", DoubleType()),
        StructField("timestamp", TimestampType())
    ])
    
    # ler stream do Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "events") \
        .option("startingOffsets", "latest") \
        .load()
    
    # converter mensagens do json pra dataframe
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # proocessar os dados
    query = parsed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    
    logger.info("Spark iniciado com sucesso!")
    return spark, query

def gerar_eventos():
    logger.info("Iniciando geração de eventos...")
    try:
        logger.info("Criando producer Kafka...")
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            acks='all',  # garantir que todas as réplicas recebam a mensagem
            retries=3    # tentar tres vezes em caso de falha
        )
        logger.info("Producer Kafka criado com sucesso!")
        
        while True:
            try:
                evento = {
                    'id': random.randint(1, 1000),
                    'valor': random.random(),
                    'timestamp': time.time()
                }
                logger.info(f"Tentando enviar evento: {evento}")
                future = producer.send('events', evento)
                # esperar a confirm do envio
                record_metadata = future.get(timeout=10)
                logger.info(f"Evento enviado com sucesso: {evento}")
                logger.info(f"Metadata: tópico={record_metadata.topic}, partição={record_metadata.partition}, offset={record_metadata.offset}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Erro ao enviar evento: {e}")
                logger.error(f"Tipo do erro: {type(e)}")
                logger.error(f"Detalhes do erro: {str(e)}")
                time.sleep(5)
    except Exception as e:
        logger.error(f"Erro ao criar producer: {e}")
        logger.error(f"Tipo do erro: {type(e)}")
        logger.error(f"Detalhes do erro: {str(e)}")

if __name__ == "__main__":
    logger.info("Iniciando aplicação...")
    
    if not esperar_kafka():
        logger.error("Não foi possível conectar ao Kafka após várias tentativas")
        exit(1)
    
    # iniciar thread de produção
    logger.info("Iniciando thread de produção...")
    produtor = threading.Thread(target=gerar_eventos)
    produtor.daemon = True  # torrnar a thread um daemon para que ela seja encerrada quando o programa principal terminar
    produtor.start()
    logger.info("Thread de produção iniciada!")
    
    # iniciar Spark
    spark, query = iniciar_spark()
    logger.info("Spark iniciado e processando eventos...")
    
    # manter o programa rodando
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Encerrando aplicação...")
        query.stop()
        spark.stop()
        produtor.join()
