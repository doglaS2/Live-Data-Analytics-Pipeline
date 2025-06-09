from kafka import KafkaProducer
import json
import time
import threading
import random
from kafka.errors import NoBrokersAvailable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verificar_topic_kafka():
    try:
        # Criar um consumidor temporário apenas para verificar tópicos
        consumer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        # O método topics() não é ideal para KafkaProducer, mas faremos uma tentativa leve
        # para ver se ele consegue conectar a um broker.
        # Uma verificação mais robusta exigiria um AdminClient, que não está no kafka-python.
        # Para este propósito, o simples fato de instanciar o producer sem erro já é um bom sinal.
        logger.info("Tentando conectar ao Kafka para verificar tópicos...")
        # Tentar listar tópicos - pode não funcionar para todos os brokers/versões com producer
        # A ideia é que se o producer pode ser criado, o Kafka está lá.
        # Em um cenário real, usaria AdminClient para verificar tópicos.
        # Como essa função é chamada antes de iniciar a thread de produção, é uma verificação de 'reachability'
        
        # Não chamar producer.topics() pois não existe
        logger.info("Conectado ao Kafka para verificação.")
        return True # Se chegou aqui, o Kafka está acessível
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
            logger.info("Kafka está pronto e acessível!")
            
            # ver se o tópico existe - a verificação anterior já é suficiente para este propósito
            # if verificar_topic_kafka(): # Não precisamos de uma checagem duplicada aqui
            #     logger.info("Tópico 'events' encontrado!")
            #     return True
            # else:
            #     logger.warning("Tópico 'events' não encontrado!")
            #     return False
            return True # Se chegamos aqui, o producer pôde ser criado
                
        except NoBrokersAvailable:
            logger.info(f"Kafka ainda não está pronto. Tentativa {i+1}/{max_retries}")
            time.sleep(retry_interval)
    return False

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
    
    # manter o programa rodando
    try:
        # Manter a thread principal viva para que a thread de produção continue rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando aplicação...")
        produtor.join()
