import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
from pyspark.sql import SparkSession
from threading import Thread

# função para gerar eventos json e jogar pro kafka
def gerar_eventos():
    """
    gera continuamente eventos simulando sensores e envia eles pra um tópico Kafka.

    O evento gerado contém:
    - sensor_id: identificador do sensor (de sensor-1 a sensor-5)
    - timestamp: data e hora atual no formato ISO 8601
    - temperatura: valor de temperatura aleatório entre 18.0 e 30.0
    - umidade: valor de umidade aleatório entre 40.0 e 90.0

    envia os eventos pro tópico kafka chamado "your_topic_name", com intervalo de 1 segundo entre cada envio.

    Args:
        None

    Returns:
        None
    """
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    def gerar_evento():
        return {
            "sensor_id": f"sensor-{random.randint(1, 5)}",
            "timestamp": datetime.utcnow().isoformat(),
            "temperatura": round(random.uniform(18.0, 30.0), 2),
            "umidade": round(random.uniform(40.0, 90.0), 2)
        }

    while True:
        evento = gerar_evento()
        print(f"Enviando: {evento}")
        producer.send("your_topic_name", evento)
        time.sleep(1)

# função principal para consumir mensagens do kafka e processá-las com Spark
def consumir_eventos():
    """
    Consome mensagens do Kafka e processa os dados usando Apache Spark.

    - Conecta-se ao tópico Kafka "your_topic_name"
    - Exibe cada mensagem recebida
    - Cria e mostra um DataFrame Spark para cada mensagem

    A sessão Spark é iniciada no início da função e parada ao final.

    Args:
        None

    Returns:
        None
    """
    # sessão Spark
    spark = SparkSession.builder \
        .appName("KafkaSparkPythonApp") \
        .getOrCreate()

    #  consumidor afka
    consumer = KafkaConsumer(
        'your_topic_name',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='your_group_id'
    )

    # processa mensagens do kafka
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
        # Exemplo: Cria um DataFrame a partir da mensagem
        df = spark.createDataFrame([(message.value.decode('utf-8'),)], ["value"])
        df.show()

    # para a sessão Spark
    spark.stop()

if __name__ == "__main__":
    """
    Ponto de entrada do script.

    Inicializa duas threads:
    - Uma para gerar e enviar eventos ao Kafka (gerar_eventos)
    - Outra para consumir e processar eventos com Spark (consumir_eventos)

    Ambas as threads são iniciadas e aguardadas até que terminem.

    Args:
        None

    Returns:
        None
    """
    # executa o gerador de eventos e o consumidor em threads separadas
    thread_produtor = Thread(target=gerar_eventos)
    thread_consumidor = Thread(target=consumir_eventos)

    thread_produtor.start()
    thread_consumidor.start()

    thread_produtor.join()
    thread_consumidor.join()
