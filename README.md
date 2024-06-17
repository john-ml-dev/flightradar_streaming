# Flight Data Streaming Project

## Overview

This project revisits a capstone project from data engineering training. It streams live flight data from [flightradar24.com](https://www.flightradar24.com/) into a Kafka topic. The data is then consumed by a front-end application like Streamlit for visualization.

## Set-Up Instructions

Follow these steps to set up the project:

1. **Install Required Libraries**

   Ensure you have all the required libraries installed in your project environment. Run the following command:

   ```shell
   pip install -r requirements.txt
2. Launch Docker Desktop App

3. Navigate to the project folder using the command

```shell
cd kafka_stream
```
4. Execute the following command to run the docker-compose.yml file:

```shell
docker compose -up -d
```

5. To connect to flightradar24.com and fetch live flight data, run the `producer.py` file.
6. The `consumer.py` file can be run to consume the live flight data

_**Note:**_ Ensure the Docker Compose file runs successfully and verify that all services are running and healthy in the Docker Desktop app before running the `producer.py` or `consumer.py` files.

Once set up, the data should stream live in your terminals.
