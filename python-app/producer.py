from kafka import KafkaProducer
import json
import time
from datetime import datetime

# Configuração do produtor
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Tópico para enviar as mensagens
topic = 'events'

# Função para gerar dados de teste
def generate_test_data():
    return {
        'timestamp': datetime.now().isoformat(),
        'value': 'Teste de mensagem',
        'id': 1
    }

# Enviando mensagens
print("Iniciando envio de mensagens...")
for i in range(5):
    data = generate_test_data()
    print(f"Enviando mensagem: {data}")
    producer.send(topic, value=data)
    time.sleep(1)  # Espera 1 segundo entre cada mensagem

print("Mensagens enviadas com sucesso!")
producer.close() 