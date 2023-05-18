import os
import requests


def sendLog(name: str, message: str):
    requests.post(
        f"http://localhost:{os.getenv('PORT', default=8000)}/log",
        json={"name": name, "message": message,
              "key": os.getenv("KEY", default="key")},
    )
