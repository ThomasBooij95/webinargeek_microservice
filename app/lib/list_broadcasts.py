import os
import pytz
import requests
from app.lib.types import BroadcastResponse
from app.lib.utils import UNIX_timestamp_to_datetime


def set_request_config():
    url: str = "https://app.webinargeek.com/api/v2/broadcasts"
    headers = {
        "Accept": "application/json",
        "Api-Token": f'{os.environ["SD_WEBINARGEEK_ACCES_TOKEN"]}',
    }
    # Prepare the initial request
    params = {"per_page": 100, "page": 1, "nested_resources": "webinar,episode"}

    return url, headers, params


def fetch_broadcast_json_webinargeek(webinar_id=None, base_url=None):
    url, headers, params = set_request_config()
    # Paginate through the results
    json_data = requests.get(url, headers=headers, params=params).json()["broadcasts"]
    # Filter the data where "isEnded" is False
    broad_cast_options = [entry for entry in json_data if not entry["has_ended"]]
    if webinar_id:
        broad_cast_options = [
            entry
            for entry in broad_cast_options
            if entry["webinar"]["id"] == webinar_id
        ]

    ret = []
    for option in broad_cast_options:
        cur = BroadcastResponse(
            id=option["id"],
            date=UNIX_timestamp_to_datetime(option["date"]).astimezone(
                pytz.timezone("Europe/Amsterdam")
            ),
            webinar_id=option["webinar"]["id"],
            title=option["webinar"]["title"],
            internal_title=option["webinar"]["internal_title"],
            webinar_url=(f"{base_url}{option['webinar']['id']}" if base_url else None),  # type: ignore
        ).dict(exclude_none=True)
        ret.append(cur)
    return ret
    # return broad_cast_options
