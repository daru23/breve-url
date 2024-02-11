import os
import redis.asyncio as redis
from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, HttpUrl
from pymongo import MongoClient

from breve import BreveURL

# TODO move this section to a config file
version = 1
api_host = "http://localhost:9000/"
origins = [
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

# Retrieve MongoDB credentials from environment variables
MONGO_DB = os.getenv("MONGO_DB")
MONGO_PORT = 27017
MONGO_HOST = "db"
# Define the MongoDB connection URL with authentication
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
breve = BreveURL(MONGO_URL, MONGO_DB)

# Rate Limit
limiter = FastAPILimiter()


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://redis:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(
        title="Breve API",
        version=version,
        openapi_url="/openapi.json",
        docs_url="/docs",
        lifespan=lifespan
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


# Schemas
class Payload(BaseModel):
    url: HttpUrl


# Routes
@app.post("/breve-me", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
@app.put("/breve-me", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def create_breve_url(payload: Payload, response_class=JSONResponse):
    try:
        # We type cast it to string because to validate the URL pydantic creates a
        # AnyURL instance of the url attribute
        url = str(payload.url)
        # Create the breve url
        breve_url = breve.breve_url(url)

        # Concat breve_url to api_host to return complete url
        response_url = api_host + breve_url
        return JSONResponse(status_code=200, content={"breve_url": response_url})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Service Temporally Unavailable"})


@app.get("/{breve_url}", response_class=RedirectResponse, dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def get_breve_url(breve_url: str):
    # Decode the breve_url and redirects to it
    decoded_url = breve.decode_url(breve_url)
    return RedirectResponse(decoded_url)
