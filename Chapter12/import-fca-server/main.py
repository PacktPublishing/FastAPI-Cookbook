from fastapi import FastAPI
from fca_server import router

app = FastAPI(title="Import FCA Server Application")

app.include_router(router)
