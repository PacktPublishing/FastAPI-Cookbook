from starlette.datastructures import MutableHeaders
from typing import Sequence


class ExtraResponseHeadersMiddleware:
    def __init__(
        self, app, headers: Sequence[tuple[str, str]]
    ):
        self.app = app
        self.headers = headers

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(
                scope, receive, send
            )

        async def send_with_extra_headers(message):
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
