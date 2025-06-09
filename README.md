# RealTime Data Pipeline com Kafka, Spark e Python

Este projeto implementa um pipeline de dados em tempo real que gera, ingere, processa e visualiza eventos contínuos utilizando Docker para orquestração. Ele integra Kafka, Spark, Druid e Metabase para processar e visualizar dados em streaming.

## Arquitetura do Sistema

```
Python App -> Gera Eventos
     ↓
   Kafka   -> Armazena Eventos
     ↓
   Druid   -> Processa e Armazena
     ↓
   Spark   -> Processa Eventos
     ↓
  Metabase -> Visualiza Dados
```

### Componentes

1. **Python App**
   - Gera eventos aleatórios (ID, valor e timestamp)
   - Envia eventos para o Kafka
   - Utiliza a biblioteca `kafka-python`

2. **Kafka**
   - Sistema de mensageria distribuído
   - Armazena os eventos em tópicos
   - Permite múltiplos consumidores

3. **Druid**
   - Processa e armazena dados em tempo real
   - Permite consultas SQL em dados de streaming
   - Componentes:
     - Coordinator (porta 8081)
     - Broker (porta 8082)
     - MiddleManager (porta 8091)

4. **Spark**
   - Processa os dados em tempo real
   - Realiza transformações nos eventos
   - Escalável para grandes volumes de dados

5. **Metabase**
   - Visualização de dados em tempo real
   - Dashboards interativos
   - Gráficos e métricas

## Tecnologias Utilizadas

- 🐍 Python (geração e envio de eventos em JSON)
- 🧭 Apache Kafka (mensageria para eventos em tempo real)
- ⚡ Apache Druid (processamento e armazenamento de dados em tempo real)
- 🔥 Apache Spark (processamento de dados em streaming)
- 📊 Metabase (visualização e dashboards)
- 🐳 Docker / Docker Compose (containerização e orquestração)

## Requisitos

- Docker instalado na máquina  
- Docker Compose instalado
- 8GB de RAM (mínimo)
- 20GB de espaço em disco
- Processador com 4 cores ou mais
- Sistema operacional Linux recomendado para melhor performance

## Estrutura do Projeto

```
docker-kafka-spark-python
├── docker-compose.yml
├── kafka/
│   └── Dockerfile
├── spark/
│   └── Dockerfile
├── python-app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Tecnologias Utilizadas

- 🐍 Python (geração e envio de eventos em JSON)
- 🧭 Apache Kafka (mensageria para eventos em tempo real)
- ⚡ Apache Druid (processamento e armazenamento de dados em tempo real)
- 🔥 Apache Spark (processamento de dados em streaming)
- 📊 Metabase (visualização e dashboards)
- 🐳 Docker / Docker Compose (containerização e orquestração)

## Requisitos

- Docker instalado na máquina  
- Docker Compose instalado
- 8GB de RAM (mínimo)
- 20GB de espaço em disco
- Processador com 4 cores ou mais
- Sistema operacional Linux recomendado para melhor performance

## Como Rodar o Projeto

1. Clone ou faça download do repositório.

2. Navegue até o diretório do projeto:

   ```bash
   cd docker-kafka-spark-python
   ```

3. Execute para construir e subir os containers:

   ```bash
   docker-compose up --build
   ```

## Como Usar

- A aplicação Python envia eventos JSON para o Kafka
- Druid ingere e processa os dados em tempo real
- Spark consome e processa esses eventos
- Metabase visualiza os dados processados
- Monitore os logs dos containers para acompanhar a atividade de cada serviço

### Acessando os Serviços

- **Druid Coordinator**: http://localhost:8081
  - Acesse "Query" para executar consultas SQL
  - Acesse "Streams" para verificar ingestão de dados

- **Metabase**: http://localhost:3000
  - Primeiro acesso: configure o banco de dados (PostgreSQL)
  - Host: metabase-db
  - Porta: 5432
  - Database: metabase
  - Usuário: metabase
  - Senha: metabase

### Exemplo de Consulta no Druid

```sql
SELECT *
FROM "events"
LIMIT 10
```

### Exemplo de Dashboard no Metabase

1. Crie uma nova pergunta
2. Selecione "Custom SQL"
3. Use a query:
```sql
SELECT 
  DATE_TRUNC('hour', timestamp) as hora,
  COUNT(*) as total_eventos,
  AVG(valor) as media_valor
FROM events
GROUP BY 1
ORDER BY 1
```

4. Visualize como gráfico de linha

## Parar os Serviços

Para interromper e remover os containers:

```bash
docker-compose down
```

## Notas Importantes

### Dependências
- O Spark requer Java 8 para funcionar corretamente
- As dependências são baixadas automaticamente na primeira execução
- O download das dependências pode levar alguns minutos

### Logs
- "Streaming query has been idle" é normal - significa que o Spark está esperando novos dados
- Os eventos são processados em lotes (batches)
- O Spark mostra estatísticas de processamento

## Solução de Problemas

### Problemas Comuns

1. **Erro de Java**
   - Verifique se está usando Java 8
   - Confira o `JAVA_HOME` no Dockerfile

2. **Kafka não inicia**
   - Verifique se o Zookeeper está rodando
   - Confira as portas no `docker-compose.yml`

3. **Spark não processa dados**
   - Verifique se o Kafka está recebendo eventos
   - Confira os logs do Spark para erros

4. **Druid não mostra dados**
   - Verifique se o Kafka está saudável
   - Confirme se o tópico "events" existe
   - Verifique os logs do Druid

5. **Metabase sem conexão**
   - Verifique se o PostgreSQL está rodando
   - Confirme as credenciais de conexão
   - Verifique os logs do Metabase

## Personalização

- Modifique `python-app/app.py` para implementar a lógica da sua aplicação
- Atualize `python-app/requirements.txt` para incluir dependências Python adicionais

## Visão Geral

Este pipeline exemplifica um fluxo típico de dados em tempo real com geração, ingestão, processamento e análise utilizando ferramentas populares. Pode ser expandido para incluir armazenamento analítico (como Apache Druid) e visualização (como Metabase).

## Próximos Passos

O pipeline pode ser estendido para:
1. Adicionar mais transformações nos dados
2. Calcular estatísticas (média, máximo, mínimo)
3. Filtrar eventos específicos
4. Agrupar eventos por critérios
5. Criar dashboards personalizados no Metabase
6. Adicionar mais visualizações e métricas

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está disponível sob a licença MIT.