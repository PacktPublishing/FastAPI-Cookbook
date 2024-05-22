import logging
from starlette.types import (
    ASGIApp,
    Scope,
    Receive,
    Send,
)
from asyncio import create_task
from httpx import AsyncClient
from fastapi import Request

client = AsyncClient()

logger = logging.getLogger("uvicorn")


async def send_webhook(url: str, event: str):
    logger.info(f"Sending event to {url}")
    try:
        await client.post(url, json={"event": event})
    except Exception as e:
        logger.error(
            f"Error sending webhook event to {url}: {e}"
        )


class WebhookSenderMiddleWare:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):
        if scope["type"] == "http":
            logger.debug(
                "Event found..."
                "sending event to the subscribed urls"
            )

            # request url
            # method
            # event
            request = Request(scope)
            urls = request.state.webhook_urls
            for url in urls:
                await send_webhook(url, "event")
                # create_task(send_webhook(url, "event"))

        await self.app(scope, receive, send)
