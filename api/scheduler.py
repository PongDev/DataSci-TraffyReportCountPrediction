from schedule import repeat, every, run_pending
import time

from api.kafka import run_kafka_producer
from api.log import sendLog


@repeat(every(1).seconds)
def kafka_producer_job():
    run_kafka_producer()


def run_scheduler():
    while True:
        try:
            run_pending()
            time.sleep(1)
        except:
            sendLog("Scheduler", "Scheduler Error")
