from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

app.mount("/", StaticFiles(directory=os.getcwd(), html=True), name="build")


@app.get("/ping", response_class=JSONResponse)
def index():
    return {"Ping": "Pong!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", default="0.0.0.0"),
        port=int(os.getenv("PORT", default=8000)),
        log_level="info",
    )
