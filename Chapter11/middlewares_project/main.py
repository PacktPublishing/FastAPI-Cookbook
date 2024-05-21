from fastapi import FastAPI, Body, APIRouter
from starlette.middleware import Middleware
from middlewares.asgi_middleware import (
    ASGIMiddleware,
    asgi_decorator,
)
from middlewares.request_modification import (
    HashBodyContentMiddleWare,
)
import logging

logger = logging.getLogger("uvicorn")

app = FastAPI(
    middleware=[
        # Middleware(asgi_decorator),
        # Middleware(ASGIMiddleware),
        Middleware(
            HashBodyContentMiddleWare,
            allowed_paths=["/send"],
        ),
    ]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/send")
async def send(message: str = Body()):
    logger.info(f"Message: {message}")
    return message
