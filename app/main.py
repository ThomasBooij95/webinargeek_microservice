from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager
from app.docs.utils import get_description
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


app = FastAPI(
    title="Booij Analytics WebinarGeek proxy",
    description=get_description(),
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
