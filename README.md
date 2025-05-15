# RealTime Data Pipeline com Kafka, Spark e Python

Este projeto implementa um pipeline de dados em tempo real que gera, ingere, processa e visualiza eventos contínuos utilizando Docker para orquestração. Ele integra Kafka, Spark e uma aplicação Python para processar dados em streaming.

---

## Estrutura do Projeto

docker-kafka-spark-python
├── docker-compose.yml
├── kafka/
│ └── Dockerfile
├── spark/
│ └── Dockerfile
├── python-app/
│ ├── Dockerfile
│ ├── app.py
│ └── requirements.txt
└── README.md


---

## Tecnologias Utilizadas

- 🐍 Python (geração e envio de eventos em JSON)
- 🧭 Apache Kafka (mensageria para eventos em tempo real)
- ⚡ Apache Spark (processamento de dados em streaming)
- 🐳 Docker / Docker Compose (containerização e orquestração)

---

## Requisitos

- Docker instalado na máquina  
- Docker Compose instalado

---

## Como Rodar o Projeto

1. Clone ou faça download do repositório.

2. Navegue até o diretório do projeto:

   ```bash
   cd docker-kafka-spark-python
Execute para construir e subir os containers:

bash
Copiar
Editar
docker-compose up --build
Como Usar
A aplicação Python envia eventos JSON para o Kafka.

Spark consome e processa esses eventos em tempo real.

Monitore os logs dos containers para acompanhar a atividade de cada serviço.

Parar os Serviços
Para interromper e remover os containers:

bash
Copiar
Editar
docker-compose down
Personalização
Modifique python-app/app.py para implementar a lógica da sua aplicação.

Atualize python-app/requirements.txt para incluir dependências Python adicionais.

Visão Geral
Este pipeline exemplifica um fluxo típico de dados em tempo real com geração, ingestão, processamento e análise utilizando ferramentas populares. Pode ser expandido para incluir armazenamento analítico (como Apache Druid) e visualização (como Metabase).

Licença
Este projeto está disponível sob a licença MIT (ou outra que desejar).
