FROM python:3.9-slim

# Instalar Java 8
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Comando para executar a aplicação
CMD ["python", "app.py"]