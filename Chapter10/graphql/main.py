from fastapi import FastAPI

from graphql_utils import graphql_app

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
