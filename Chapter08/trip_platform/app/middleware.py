import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("uvicorn")


class ClientInfoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host_client = request.client.host
        requested_path = request.url.path
        method = request.method

        logger.info(
            f"host client {host_client} "
            f"requested {method} {requested_path} "
            "endpoint"
        )

        return await call_next(request)
