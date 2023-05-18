from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import multiprocessing
import uvicorn
import os
from api.kafka import run_kafka_consumer
from api.scheduler import run_scheduler
from pydantic import BaseModel


class LogData(BaseModel):
    name: str
    message: str
    key: str


app = FastAPI()


@app.get("/ping", response_class=JSONResponse)
def index():
    return {"Ping": "Pong!"}


@app.post("/log")
def receiveLog(logData: LogData):
    if logData.key == os.getenv("KEY", default="key"):
        print(f"[{logData.name}] {logData.message}")
    return None


app.mount("/", StaticFiles(directory=os.getcwd(), html=True), name="build")

if __name__ == "__main__":
    kafkaConsumer = multiprocessing.Process(target=run_kafka_consumer)
    kafkaConsumer.start()

    scheduler = multiprocessing.Process(target=run_scheduler)
    scheduler.start()

    uvicorn.run(
        app,
        host=os.getenv("HOST", default="0.0.0.0"),
        port=int(os.getenv("PORT", default=8000)),
        log_level="info",
    )
    print("API Server Terminated")

    kafkaConsumer.terminate()
    print("Kafka Consumer Terminated")

    scheduler.terminate()
    print("Scheduler Terminated")
