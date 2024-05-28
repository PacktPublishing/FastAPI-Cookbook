from fastapi import FastAPI

app = FastAPI(title="FastAPI Cookbook Application")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI Cookbook Application!"
    }
