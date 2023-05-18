from kafka import KafkaConsumer, KafkaProducer
import os
import time
import schedule
from api.log import sendLog


def run_kafka_consumer():
    while True:
        try:
            kafka_broker = os.getenv("KAFKA_HOST", default="localhost:9092")

            consumer = KafkaConsumer(
                "data",
                bootstrap_servers=[kafka_broker],
                enable_auto_commit=True,
                value_deserializer=lambda x: x.decode("utf-8"),
            )

            sendLog("Kafka Consumer", "Starting Kafka Consumer")
            for message in consumer:
                sendLog(
                    "Kafka Consumer",
                    f"[{message.timestamp}:{message.offset}] {message.value}",
                )
        except:
            sendLog("Kafka Consumer", "Kafka Consumer: Error")
            time.sleep(1)


def run_kafka_producer():
    kafka_broker = os.getenv("KAFKA_HOST", default="localhost:9092")

    producer = KafkaProducer(
        bootstrap_servers=[kafka_broker],
    )

    sendLog("Kafka Producer", f"Execute Kafka Producer: {kafka_broker}")
    data = "Hello World!"
    producer.send("data", data.encode("utf-8"))
