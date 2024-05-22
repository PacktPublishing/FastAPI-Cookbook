import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import APIRouter, Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware,
)
from pydantic import BaseModel
from starlette.middleware import Middleware

from middlewares.asgi_middleware import (
    ASGIMiddleware,
    asgi_decorator,
)
from middlewares.request_modification import (
    HashBodyContentMiddleWare,
)
from middlewares.response_modification import (
    ExtraResponseHeadersMiddleware,
)
from middlewares.webhook import (
    WebhookSenderMiddleWare,
)

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"webhook_urls": []}


app = FastAPI(
    lifespan=lifespan,
    middleware=[
        # Middleware(asgi_decorator),
        # Middleware(ASGIMiddleware),
        Middleware(
            HashBodyContentMiddleWare,
            allowed_paths=["/send"],
        ),
        Middleware(
            ExtraResponseHeadersMiddleware,
            headers=(
                ("new-header", "fastapi-cookbook"),
                (
                    "another-header",
                    "fastapi-cookbook",
                ),
            ),
        ),
    ],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/send")
async def send(message: str = Body()):
    logger.info(f"Message: {message}")
    return message


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost"],
)


@app.post("/webhooks-url")
async def add_webhook_url(
    request: Request, url: str = Body()
):
    if not url.startswith("http"):
        url = f"http://{url}"
    request.state.webhook_urls.append(url)
    return {"url added": url}


app.add_middleware(
    WebhookSenderMiddleWare,
)


class Subscription(BaseModel):
    username: str
    # monthly_fee: float
    # start_date: datetime


@app.webhooks.post("/subscribe")
def subscribe(subscription: Subscription):
    """_summary_

    Args:
        subscription (Subscription): _description_
    """
    print("arrivato")


from submain import subapp

app.mount("/subapp", subapp)
