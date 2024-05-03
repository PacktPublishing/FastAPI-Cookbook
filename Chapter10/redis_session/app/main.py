import uuid

from fastapi import FastAPI, Request, Response
from redis import asyncio as aioredis

app = FastAPI()

redis_client = aioredis.from_url("redis://localhost")


async def session_middleware(
    request: Request, call_next
):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_data = await redis_client.get(
            f"session:{session_id}"
        )
        request.state.session = session_data
    else:
        session_id = str(uuid.uuid4())
        request.state.session = {}
    response = await call_next(request)
    response.set_cookie("session_id", session_id)
    await redis_client.set(
        f"session:{session_id}",
        request.state.session,
    )
    return response


app.middleware("http")(session_middleware)
