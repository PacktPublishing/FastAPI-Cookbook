import logging
import functools
from starlette.types import (
    ASGIApp,
    Scope,
    Receive,
    Send,
)

logger = logging.getLogger("uvicorn")


class ASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):
        logger.info(
            f"ASGI scope: {scope.get('type')}"
        )
        logger.info(f"ASGI send: {send}")
        await self.app(scope, receive, send)
        logger.info(  # include shutdown in the recipe
            f"ASGI scope after shutdown: {scope.get('type')}"
        )


def asgi_decorator(app):
    @functools.wraps(app)
    async def wrapped_app(scope, receive, send):
        logger.info(
            f"ASGI scope decorated function: {scope.get('type')}"
        )

        await app(scope, receive, send)

    return wrapped_app
