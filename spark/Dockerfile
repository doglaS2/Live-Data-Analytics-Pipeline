FROM bitnami/spark:3.5.0

USER root

WORKDIR /opt/spark-app

COPY app.py /opt/spark-app/

RUN chown -R 1001:1001 /opt/spark-app && \
    mkdir -p /tmp/checkpoint && \
    chown -R 1001:1001 /tmp/checkpoint

USER 1001

ENV PATH="/opt/bitnami/spark/bin:${PATH}"
ENV JAVA_OPTS="-Djava.net.preferIPv4Stack=true -XX:+UseG1GC -XX:MaxGCPauseMillis=200"

CMD ["/opt/bitnami/spark/bin/spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", \
     "--conf", "spark.sql.streaming.checkpointLocation=/tmp/checkpoint", \
     "--conf", "spark.driver.extraJavaOptions=-Djava.net.preferIPv4Stack=true", \
     "--conf", "spark.executor.extraJavaOptions=-Djava.net.preferIPv4Stack=true", \
     "/opt/spark-app/app.py"]