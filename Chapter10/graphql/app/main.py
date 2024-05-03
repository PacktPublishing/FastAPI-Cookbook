from fastapi import FastAPI


from app.graphql import graphql_app

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
