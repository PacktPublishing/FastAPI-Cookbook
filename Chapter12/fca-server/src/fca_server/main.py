from fastapi import APIRouter

router = APIRouter()


@router.get("/home")
def read_root():
    return {
        "message": "Welcome to the FastAPI Cookbook Application!"
    }
