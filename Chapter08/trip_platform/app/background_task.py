import asyncio
import logging

logger = logging.getLogger("uvicorn.error")


async def store_query_to_external_db(message: str):
    logger.info(f"Storing message '{message}'.")
    await asyncio.sleep(2)
    logger.info(f"Message '{message}' stored!")
