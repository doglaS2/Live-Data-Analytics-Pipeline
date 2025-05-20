# Jogo das Letras: A Batalha do Lago Lexis

Jogo desenvolvido em Java 11 utilizando matrizes para implementar um tabuleiro 3x3. Sistema de jogo baseado em estratégia com validação de jogadas e persistência de dados.

Um jogo de estratégia em Java onde letras maiúsculas e minúsculas competem em um tabuleiro 3x3. Forme sequências de três letras enquanto usa estratégias de superioridade entre letras para vencer.

<div align ="center">
  <img src="https://img.shields.io/badge/Java-11-orange" alt="Java 11">
  <img src="https://img.shields.io/badge/Licença-MIT-blue" alt="Licença MIT">
  <img src="https://img.shields.io/badge/Versão-1.0-green" alt="Versão 1.0">
</div>

## 📖 A História

// ... existing code ...

## 📁 Estrutura do Projeto

```
letter_game/
├── src/
│   ├── models/
│   │   └── Matriz.java
│   ├── utils/
│   │   └── EscritaArquivo.java
│   └── game/
│       └── LetterGame.java
├── pom.xml
└── README.md
```

## 🛠️ Tecnologias Utilizadas

- 🐍 Python (geração e envio de eventos em JSON)
- 🧭 Apache Kafka (mensageria para eventos em tempo real)
- ⚡ Apache Spark (processamento de dados em streaming)
- 🐳 Docker / Docker Compose (containerização e orquestração)

## 📋 Requisitos

- Docker instalado na máquina
- Docker Compose instalado

## 🚀 Como Rodar o Projeto

1. Clone ou faça download do repositório.

2. Navegue até o diretório do projeto:
   ```bash
   cd docker-kafka-spark-python
   ```

3. Execute para construir e subir os containers:
   ```bash
   docker-compose up --build
   ```

## 🎮 Como Usar

- A aplicação Python envia eventos JSON para o Kafka
- Spark consome e processa esses eventos em tempo real
- Monitore os logs dos containers para acompanhar a atividade de cada serviço

## ⏹️ Parar os Serviços

Para interromper e remover os containers:
```bash
docker-compose down
```

## 🔧 Personalização

- Modifique `python-app/app.py` para implementar a lógica da sua aplicação
- Atualize `python-app/requirements.txt` para incluir dependências Python adicionais

## 📊 Visão Geral

Este pipeline exemplifica um fluxo típico de dados em tempo real com geração, ingestão, processamento e análise utilizando ferramentas populares. Pode ser expandido para incluir armazenamento analítico (como Apache Druid) e visualização (como Metabase).

// ... rest of existing code ...