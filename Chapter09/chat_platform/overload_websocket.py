import multiprocessing
from random import random

import uvicorn
from websockets import connect

from app.main import app


def run_server():
    uvicorn.run(app)


async def connect_client(n: int):
    async with connect(
        f"ws://localhost:8000/ws-for-test/user{n}",
        timeout=None,
        ping_timeout=None,
        ping_interval=None,
    ) as client:
        # client = await connect(
        #    f"ws://localhost:8000/ws-for-test/{username}",
        #    timeout=float("inf"),
        #    ping_timeout=None,
        #    ping_interval=None,
        # )

        for _ in range(3):
            await client.send(
                f"Hello World from user{n}"
            )
            await asyncio.sleep(n * 0.1)
        await asyncio.sleep(2)


async def main():
    p = multiprocessing.Process(target=run_server)
    p.start()

    connections = [
        connect_client(n) for n in range(100)
    ]

    await asyncio.gather(*connections)

    await asyncio.sleep(1)
    p.terminate()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
