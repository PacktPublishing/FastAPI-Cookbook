from fastapi import FastAPI
from starlette.middleware import Middleware
from asgi_middleware import (
    ASGIMiddleware,
    asgi_decorator,
)

app = FastAPI(
    middleware=[Middleware(asgi_decorator), Middleware(ASGIMiddleware)]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
