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
from pydantic import BaseModel
from datetime import datetime


client = AsyncClient()

logger = logging.getLogger("uvicorn")


class Event(BaseModel):
    host: str
    path: str
    time: str
    body: dict | None = None


async def send_event_to_url(url: str, event: Event):
    logger.info(f"Sending event to {url}")
    try:
        await client.post(
            f"{url}/fastapi-webhook",
            json={"event": event},
        )
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
            request = Request(scope)
            event = Event(
                host=request.client.host,
                path=request.url.path,
                time=datetime.now().isoformat(),
                body=await request.json(),
            )
            urls = request.state.webhook_urls
            for url in urls:
                await send_event_to_url(url, event)
                # create_task(send_webhook(url, "event"))

        await self.app(scope, receive, send)
