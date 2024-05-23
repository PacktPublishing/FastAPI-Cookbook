from typing import Sequence

from starlette.datastructures import MutableHeaders
from starlette.types import (
    ASGIApp,
    Receive,
    Scope,
    Send,
    Message,
)


class ExtraHeadersResponseMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        headers: Sequence[tuple[str, str]],
    ):
        self.app = app
        self.headers = headers

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):
        if scope["type"] != "http":
            return await self.app(
                scope, receive, send
            )

        async def send_with_extra_headers(
            message: Message,
        ):
            if (
                message["type"]
                == "http.response.start"
            ):
                headers = MutableHeaders(
                    scope=message
                )
                for key, value in self.headers:
                    headers.append(key, value)

            await send(message)

        await self.app(
            scope, receive, send_with_extra_headers
        )
