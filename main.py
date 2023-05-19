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
import pickle
import pandas as pd
import numpy as np
import requests


class LogData(BaseModel):
    name: str
    message: str
    key: str


class CommandData(BaseModel):
    command: str
    key: str


with open("sidewalk_model.pkl", "rb") as f:
    sidewalk_model = pickle.load(f)
with open("light_model.pkl", "rb") as f:
    light_model = pickle.load(f)
with open("road_model.pkl", "rb") as f:
    road_model = pickle.load(f)

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
async def addDataRoute(data: DBData):
    if data.key == os.getenv("KEY", default="key"):
        await addData(
            {
                "date": data.date,
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
        return "OK"
    return None


@app.post("/command")
async def command(command: CommandData):
    if command.key == os.getenv("KEY", default="key"):
        if command.command == "loadData":
            await preloadData()
            return "OK"
    return None


@app.get("/predict")
def predict():
    region_list = [
        "กรุงธนเหนือ",
        "กรุงเทพกลาง",
        "กรุงธนใต้",
        "กรุงเทพตะวันออก",
        "กรุงเทพใต้",
        "กรุงเทพเหนือ",
    ]
    rinfo = {
        "กรุงธนเหนือ": [150.049, 739081, 4925.597638],
        "กรุงธนใต้": [300.070, 955968, 3185.816643],
        "กรุงเทพกลาง": [78.921, 610303, 7733.087518],
        "กรุงเทพตะวันออก": [693.879, 1364124, 1965.939306],
        "กรุงเทพเหนือ": [212.992, 1048444, 4922.457181],
        "กรุงเทพใต้": [132.830, 777012, 5849.672514],
    }
    x = requests.get(
        f"http://localhost:{os.getenv('PORT', default=8000)}/get_data",
    )
    df = pd.DataFrame(x.json())
    averages = []
    for i, reg in enumerate(region_list):
        df_r = (
            df[df["region"] == reg].sort_values(
                "date").drop(columns=["region", "date"])
        )
        arr = df_r.values[::-1].mean(axis=0)
        averages.append(list(arr))
    averages = np.array(averages)
    response = {}
    input = []
    for i, reg in enumerate(region_list):
        df_r = (
            df[df["region"] == reg].sort_values(
                "date").drop(columns=["region", "date"])
        )
        arr = list(df_r.values[::-1].reshape(-1)) + rinfo[reg]
        arr.append(i)
        arr.append(int(datetime.now().weekday() ==
                   5 or datetime.now().weekday() == 6))
        input.append(arr)
    input = np.array(input)
    prediction_sidewalk = sidewalk_model.predict(input)
    prediction_light = light_model.predict(input)
    prediction_road = road_model.predict(input)
    response = {}
    for i, reg in enumerate(region_list):
        response[reg + "_sidewalk"] = prediction_sidewalk[input[:, -2] == i][0]
        response[reg + "_light"] = prediction_light[input[:, -2] == i][0]
        response[reg + "_road"] = prediction_road[input[:, -2] == i][0]
    for day in range(1, 3):
        temp = averages.copy()
        for j in range(6):
            temp[j, 6] = prediction_road[input[:, -2] == i][0]
            temp[j, 7] = prediction_sidewalk[input[:, -2] == i][0]
            temp[j, 12] = prediction_light[input[:, -2] == i][0]
        input = np.concatenate([temp, input[:, :78], input[:, -5:]], axis=1)
        prediction_sidewalk = sidewalk_model.predict(input)
        prediction_light = light_model.predict(input)
        prediction_road = road_model.predict(input)
        for i, reg in enumerate(region_list):
            response[reg + f"_sidewalk_{day}"] = prediction_sidewalk[input[:, -2] == i][
                0
            ]
            response[reg +
                     f"_light_{day}"] = prediction_light[input[:, -2] == i][0]
            response[reg +
                     f"_road_{day}"] = prediction_road[input[:, -2] == i][0]
    return response


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
