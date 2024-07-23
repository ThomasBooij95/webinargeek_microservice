import requests
from dotenv import load_dotenv
import os

load_dotenv()


def set_request_config():
    url: str = "https://app.webinargeek.com/api/v2/broadcasts"
    headers = {
        "Accept": "application/json",
        "Api-Token": f'{os.getenv("SD_WEBINARGEEK_ACCES_TOKEN")}',
    }
    # Prepare the initial request
    params = {"per_page": 100, "page": 1}

    return url, headers, params


def fetch_broadcast_json_webinargeek():
    url, headers, params = set_request_config()
    # Paginate through the results
    json_data = requests.get(url, headers=headers, params=params).json()["broadcasts"]
    # Filter the data where "isEnded" is False
    broad_cast_options = [entry for entry in json_data if entry["has_ended"] == False]
    return broad_cast_options
