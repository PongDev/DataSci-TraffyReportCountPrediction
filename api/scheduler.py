from schedule import repeat, every, run_pending
import time

from api.kafka import run_kafka_producer


@repeat(every(1).seconds)
def kafka_producer_job():
    run_kafka_producer()


def run_scheduler():
    while True:
        run_pending()
        time.sleep(1)
