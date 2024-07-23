from fastapi import FastAPI

from app.list_broadcasts import fetch_broadcast_json_webinargeek
import json

app = FastAPI()
from dotenv import load_dotenv

load_dotenv()


@app.get("/")
def read_main():
    data = fetch_broadcast_json_webinargeek()
    return data
