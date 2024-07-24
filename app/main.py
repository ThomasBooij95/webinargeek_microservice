from fastapi import FastAPI

import json

from lib.list_broadcasts import fetch_broadcast_json_webinargeek

app = FastAPI()
from dotenv import load_dotenv

load_dotenv()


@app.get("/list_broadcasts")
def list_available_broadcasts():
    return fetch_broadcast_json_webinargeek()
