from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager
from app.lib.types import BroadcastResponse
from fastapi import FastAPI, Response, Request
from fastapi_cache.backends.redis import RedisBackend
from app.lib.list_broadcasts import fetch_broadcast_json_webinargeek


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host="redis", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()


description = """
# Welcome to the WebinarGeek API Documentation

Welcome to the API documentation for WebinarGeek's broadcast listing service, powered by FastAPI. This API allows you to fetch information about available broadcasts efficiently, leveraging the power of caching for optimized performance.

## Key Features

- **Fast and Modern**: Built with FastAPI, one of the fastest Python frameworks, ensuring high performance and low latency.
- **Flexible Endpoints**: Retrieve broadcast data using optional query parameters, making it easy to get the information you need.
- **Efficient Caching**: Utilizes caching to reduce load times and improve user experience by storing responses for 15 minutes.

## Getting Started

Our API is designed to be straightforward and intuitive. Here’s a brief overview to get you started:

### Base URL

The base URL for accessing the API is:
stresslessdogs.booijanalytics.nl/

### Endpoints

#### List Available Broadcasts

Fetches information about available broadcasts. You can optionally specify a `webinar_id` to get data for a specific webinar.

- **URL**: `/list_broadcasts/`
- **Method**: `GET`
- **Query Parameters**:
  - `webinar_id` (optional, integer): The ID of the webinar to fetch broadcasts for.

##### Example Requests

1. **Fetch all broadcasts**:
GET /list_broadcasts/


2. **Fetch broadcasts for a specific webinar**:
GET /list_broadcasts/?webinar_id=123



##### Response

The response will be a JSON object containing the broadcast data. If a `webinar_id` is provided, the data will pertain to that specific webinar. Otherwise, it will return default broadcast data.

```json
{
"data": "Broadcast data",
"webinar_id": 123  // if applicable
}




"""
app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Microservice for fetching broadcasts and subscribing users.",
    version="1.0.1",
    terms_of_service="https://www.booijanalytics.nl/",
    contact={
        "name": "Thomas Booij",
        "url": "https://www.booijanalytics.nl/",
        "email": "thomas@booijanalytics.nl",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan,
)


@app.get("/")
async def health_check():
    return Response("The server is running")


@app.get("/list_broadcasts/")
@cache(expire=900)  # Cache expires after 15 minutes (900 seconds)
async def list_available_broadcasts(request_object: Request) -> list[BroadcastResponse]:
    return fetch_broadcast_json_webinargeek(base_url=str(request_object.url))


@app.get("/list_broadcasts/{webinar_id}")
@cache(expire=900)  # Cache expires after 15 minutes (900 seconds)
async def list_available_broadcasts_of_webinar(
    webinar_id: int,
) -> list[BroadcastResponse]:
    return fetch_broadcast_json_webinargeek(webinar_id)
