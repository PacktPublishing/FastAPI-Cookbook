from fastapi import FastAPI

app = FastAPI(title="FastAPI Live Application")


@app.get("/")
def read_root():
    return {"Hello": "World"}
