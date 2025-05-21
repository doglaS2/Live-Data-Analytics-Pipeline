FROM bitnami/spark:latest

USER root

WORKDIR /opt/spark-app

COPY app.py /opt/spark-app/

RUN chown -R 1001:1001 /opt/spark-app

USER 1001

ENV PATH="/opt/bitnami/spark/bin:${PATH}"

CMD ["/opt/bitnami/spark/bin/spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0", "/opt/spark-app/app.py"]