# RealTime Data Pipeline com Kafka, Spark e Python

Este projeto implementa um pipeline de dados em tempo real que gera, ingere, processa e visualiza eventos contínuos utilizando Docker para orquestração. Ele integra Kafka, Spark e uma aplicação Python para processar dados em streaming.

## Arquitetura do Sistema

```
Python App -> Gera Eventos
     ↓
   Kafka   -> Armazena Eventos
     ↓
   Spark   -> Processa Eventos
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

3. **Spark**
   - Processa os dados em tempo real
   - Realiza transformações nos eventos
   - Escalável para grandes volumes de dados

## Tecnologias Utilizadas

### Por que Python?
- Linguagem fácil de usar
- Boas bibliotecas para Kafka
- Ideal para scripts e automação

### Por que Java?
- Necessário para Spark e Kafka
- Spark é escrito em Java
- Kafka é escrito em Java
- Muitas ferramentas de Big Data usam Java como base

### Por que Debian?
- Base da imagem Python oficial
- Mais leve que Ubuntu
- Mais estável
- Usamos a imagem `python:3.9-slim`

### Por que Docker?
- Isola cada componente
- Garante versões consistentes
- Fácil de executar em qualquer máquina
- Simplifica a configuração do ambiente

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
- ⚡ Apache Spark (processamento de dados em streaming)
- 🐳 Docker / Docker Compose (containerização e orquestração)

## Requisitos

- Docker instalado na máquina  
- Docker Compose instalado
- 4GB de RAM (mínimo)
- 10GB de espaço em disco

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
- Spark consome e processa esses eventos em tempo real
- Monitore os logs dos containers para acompanhar a atividade de cada serviço

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
5. Adicionar visualização dos dados

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está disponível sob a licença MIT.