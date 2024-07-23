from fastapi import FastAPI

import json

from lib.list_broadcasts import fetch_broadcast_json_webinargeek

app = FastAPI()
from dotenv import load_dotenv

load_dotenv()


@app.get("/")
def read_main():
    data = fetch_broadcast_json_webinargeek()
    return {"Hello world"}
