from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()

app.mount("/", StaticFiles(directory="build", html=True))


@app.get("/ping", response_class=JSONResponse)
def index():
    return {"Ping": "Pong!"}
