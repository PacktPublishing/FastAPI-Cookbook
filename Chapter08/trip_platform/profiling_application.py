import asyncio
import time
from contextlib import contextmanager
from multiprocessing import Process

import uvicorn
from httpx import AsyncClient

from app.main import app
from app.profiler import ProfileEndpointsMiddleWare


def run_server():
    app.add_middleware(ProfileEndpointsMiddleWare)
    uvicorn.run(app, port=8000)


@contextmanager
def run_server_in_process():
    p = Process(target=run_server)
    p.start()
    time.sleep(2)  # Give the server a second to start
    yield
    p.terminate()


async def make_requests(n: int):
    async with AsyncClient(
        base_url="http://localhost:8000"
    ) as client:
        tasks = (
            client.get(
                "/sleeping_sync", timeout=float("inf")
            )
            for _ in range(n)
        )

        await asyncio.gather(*tasks)


async def main():
    with run_server_in_process():
        # Make requests to the server
        print("Server is running in a separate process")
        await make_requests(2)


if __name__ == "__main__":
    asyncio.run(main())
