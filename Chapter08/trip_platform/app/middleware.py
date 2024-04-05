from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next
    ):
        # do something with the request object, for example
        content_type = request.headers.get(
            "Content-Type"
        )
        # to get the client host request.client.host
        print(content_type)

        # process the request and get the response
        response = await call_next(request)

        return response
