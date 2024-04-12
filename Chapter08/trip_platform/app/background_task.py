import asyncio
import logging

logger = logging.getLogger("uvicorn.error")


async def store_query_to_external_source(message: str):
    logger.info(
        f"Storing message '{message}' "
        "to external source"
    )
    await asyncio.sleep(2)
    logger.info(
        f"Message '{message}' successfully stored"
    )
