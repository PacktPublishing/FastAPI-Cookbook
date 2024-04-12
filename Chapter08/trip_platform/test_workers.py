import asyncio
import multiprocessing
import time

import uvicorn
from httpx import AsyncClient

from app.main import app


def run_app(workers: int):
    uvicorn.run(app, port=8000, workers=workers)


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
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
        print(
            f"Time taken with {n} requests: {end_time - start_time} seconds"
        )
        return end_time - start_time


# To stop the thread, you can use the `thread.join()` method.
# This will block the main thread until the `run_app` thread completes.
async def main():
    p = multiprocessing.Process(
        target=run_app, args=(1,)
    )
    p.start()
    time.sleep(5)  # Give the server a second to start
    time_one_worker = await make_requests(10)
    p.terminate()

    p = multiprocessing.Process(
        target=run_app, args=(5,)
    )
    p.start()
    time.sleep(5)  # Give the server a second to start
    time_3_workers = await make_requests(10)
    p.terminate()

    print("With one worker:", time_one_worker)
    print("With three workers:", time_3_workers)


if __name__ == "__main__":
    asyncio.run(main())
