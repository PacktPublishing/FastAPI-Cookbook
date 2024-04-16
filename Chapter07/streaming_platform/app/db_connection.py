import logging

from elasticsearch import (
    AsyncElasticsearch,
    TransportError,
)
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis

logger = logging.getLogger("uvicorn")


mongo_client = AsyncIOMotorClient(
    "mongodb://localhost:27017"
)

es_client = AsyncElasticsearch("http://localhost:9200")

redis_client = aioredis.from_url("redis://localhost")


async def ping_mongo_db_server():
    try:
        await mongo_client.admin.command("ping")
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(
            f"Error connecting to MongoDB: {e}"
        )
        raise e


async def ping_elasticsearch_server():
    try:
        await es_client.info()
        logger.info(
            "Elasticsearch connection successful"
        )
    except TransportError as e:
        logger.error(
            f"Elasticsearch connection failed: {e}"
        )
        # raise e


async def ping_redis_server():
    try:
        await redis_client.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        # raise e
