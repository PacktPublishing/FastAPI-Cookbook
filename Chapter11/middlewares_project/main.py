from fastapi import FastAPI, Body, APIRouter
from starlette.middleware import Middleware
from middlewares.asgi_middleware import (
    ASGIMiddleware,
    asgi_decorator,
)
from middlewares.request_modification import (
    HashBodyContentMiddleWare,
)
from starlette.middleware import Middleware
from middlewares.response_modification import (
    ExtraResponseHeadersMiddleware,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware,
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
    ]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/send")
async def send(message: str = Body()):
    logger.info(f"Message: {message}")
    return message


#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost"],
)

subapp = FastAPI()


@subapp.get("/")
async def read_root_sub():
    return {"Hello": "World from subapp"}


app.mount("/subapp", subapp)
