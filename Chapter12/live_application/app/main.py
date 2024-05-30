import logging
from os import getpid

from fastapi import FastAPI

"""
Uncomment the following lines to
enable HTTPS redirection
only works when the server is running with HTTPS
"""

# from fastapi.middleware.httpsredirect import (
#     HTTPSRedirectMiddleware,
# )

logger = logging.getLogger("uvicorn")

app = FastAPI(title="FastAPI Live Application")

# app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
def read_root():
    logger.info(f"Processd by worker {getpid()}")
    return {"Hello": "World"}
