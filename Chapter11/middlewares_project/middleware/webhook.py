import logging
from asyncio import create_task
from datetime import datetime

from fastapi import Request
from httpx import AsyncClient
from pydantic import BaseModel
from starlette.types import (
    ASGIApp,
    Receive,
    Scope,
    Send,
)


class Event(BaseModel):
    host: str
    path: str
    time: str
    body: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "127.0.0.1",
                    "path": "/send",
                    "time": "2024-05-22T14:24:28.847663",
                    "body": '"body content"',
                }
            ]
        }
    }


client = AsyncClient()

logger = logging.getLogger("uvicorn")


async def send_event_to_url(url: str, event: Event):
    logger.info(f"Sending event to {url}")
    try:
        await client.post(
            f"{url}/fastapi-webhook",
            json=event.model_dump(),
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
            message = await receive()
            body = message.get("body", b"")
            request = Request(scope=scope)

            event = Event(
                host=request.client.host,
                path=request.url.path,
                time=datetime.now().isoformat(),
                body=body,
            )
            urls = request.state.webhook_urls
            for url in urls:
                await create_task(
                    send_event_to_url(url, event)
                )

            async def continue_receive():
                return message

            await self.app(
                scope, continue_receive, send
            )
            return

        await self.app(scope, receive, send)
