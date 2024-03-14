import logging

from motor.motor_asyncio import AsyncIOMotorClient

logger = logger = logging.getLogger("uvicorn.error")


client = AsyncIOMotorClient("mongodb://localhost:27017")


async def ping_server():
    try:
        await client.admin.command("ping")
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(
            f"Error connecting to MongoDB: {e}"
        )
        raise e
