from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import multiprocessing
import uvicorn
import os
from api.kafka import run_kafka_consumer
from api.data import addData, DBData, preloadData, getData
from api.scheduler import run_scheduler
from pydantic import BaseModel
from datetime import datetime


class LogData(BaseModel):
    name: str
    message: str
    key: str


class CommandData(BaseModel):
    command: str
    key: str


app = FastAPI()


@app.get("/ping", response_class=JSONResponse)
def index():
    return {"Ping": "Pong!"}


@app.get("/get_data")
async def getDataRoute():
    return await getData()


@app.post("/log")
def receiveLog(logData: LogData):
    if logData.key == os.getenv("KEY", default="key"):
        print(f"[{logData.name}] {logData.message}")
    return None


@app.post("/add_data")
def addDataRoute(data: DBData):
    addData(
        {
            "date": datetime.strptime(data.date, "%Y-%m-%d"),
            "region": data.region,
            "obstacle": data.obstacle,
            "canal": data.canal,
            "security": data.security,
            "sanitary": data.sanitary,
            "traffic": data.traffic,
            "road": data.road,
            "sidewalk": data.sidewalk,
            "sewer": data.sewer,
            "flood": data.flood,
            "bridge": data.bridge,
            "electricWire": data.electricWire,
            "light": data.light,
            "tree": data.tree,
        }
    )


@app.post("/command")
async def command(command: CommandData):
    if command.key == os.getenv("KEY", default="key"):
        if command.command == "loadData":
            await preloadData()
            return "OK"
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
