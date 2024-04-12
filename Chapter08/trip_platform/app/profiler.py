import asyncio
import os
from contextlib import asynccontextmanager
from time import sleep

from fastapi import APIRouter, FastAPI, Request
from pyinstrument import Profiler
from pyinstrument.renderers.speedscope import (
    SpeedscopeRenderer,
)
from starlette.middleware.base import BaseHTTPMiddleware

profiler = Profiler(
    interval=0.0001, async_mode="enabled"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    profiler.start()
    yield
    profiler.stop()
    profiler.write_html(os.getcwd() + "/profiler.html")


class ProfileEndpointsMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next
    ):
        if not profiler.is_running:
            profiler.start()
        response = await call_next(request)
        if profiler.is_running:
            profiler.stop()
            with open(
                os.getcwd() + "/profiler2.json", "w"
            ) as file:
                file.write(
                    profiler.output(
                        SpeedscopeRenderer()
                    )
                )
            profiler.write_html(
                os.getcwd() + "/profiler.html"
            )
            profiler.start()
        return response


router = APIRouter(tags=["Profiler Endpoints"])


@router.get("/sleeping")
async def sleeping_endpoint():
    await asyncio.sleep(5)
    print("after sleep")
    return {"message": "I slept for 5 seconds"}


@router.get("/sleeping1")
async def sleeping_endpoint1():
    await asyncio.sleep(2)
    print("after sleep 1")
    return {"message": "I slept for 5 seconds"}


@router.get("/sleeping_sync")
async def sleeping_sync():
    sleep(10)
    return {"message": "I slept for 2 seconds"}


# TODO check how to cumulate the stats and setup the specific endpoint
# build two endpoints with some sleeping time in it
# write a test that calls both endpoints, then check the stats
# make a first improuvement by adding a worker, then another
# by using asynchrounous calls in between
# you can also profile the tests directly to show the difference
# this will probably be with timeit (to check)
# @app.middleware("http")
# async def profile_request(request: Request, call_next):
#    if request.url.path in ["/docs", "/openapi.json"]:
#        return await call_next(request)
#    profiler.start()
#    await call_next(request)
#    profiler.stop()
#    return HTMLResponse(profiler.output_html())
