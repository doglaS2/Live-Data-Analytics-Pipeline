# Docker Kafka Spark Python Project

This project sets up a basic application using Docker that integrates Kafka, Spark, and a Python application. Below are the details for setting up and running the project.

## Project Structure

```
docker-kafka-spark-python
├── docker-compose.yml
├── kafka
│   └── Dockerfile
├── spark
│   └── Dockerfile
├── python-app
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Prerequisites

- Docker installed on your machine
- Docker Compose installed

## Setup Instructions

1. Clone the repository or download the project files to your local machine.

2. Navigate to the project directory:

   ```
   cd docker-kafka-spark-python
   ```

3. Build and start the services using Docker Compose:

   ```
   docker-compose up --build
   ```

   This command will build the Docker images for Kafka, Spark, and the Python application, and start the containers.

## Usage

- Once the services are running, you can interact with the Python application, which connects to Kafka and processes data using Spark.
- You can access the logs of each service to monitor their activity.

## Stopping the Services

To stop the services, you can use:

```
docker-compose down
```

This command will stop and remove the containers created by Docker Compose.

## Additional Information

- Modify the `python-app/app.py` file to implement your application logic.
- Update `python-app/requirements.txt` to add any additional Python dependencies required for your application.

For further details on Kafka, Spark, and Docker, refer to their respective documentation.