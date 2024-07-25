from dotenv import load_dotenv
from fastapi import FastAPI
from lib.list_broadcasts import fetch_broadcast_json_webinargeek

app = FastAPI()

load_dotenv()


# add a comment
@app.get("/list_broadcasts_maria_me_gusta")
def list_available_broadcasts():
    return fetch_broadcast_json_webinargeek()
