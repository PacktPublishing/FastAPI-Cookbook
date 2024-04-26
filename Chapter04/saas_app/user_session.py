from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db_connection import get_session
from operations import get_user
from rbac import get_current_user
from responses import UserCreateResponse

router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    user: UserCreateResponse = Depends(
        get_current_user
    ),
    session: Session = Depends(get_session),
):
    user = get_user(session, user.username)

    response.set_cookie(
        key="fakesession", value=f"{user.id}"
    )
    return {"message": "User logged in successfully"}


@router.post("/logout")
async def logout(
    response: Response,
    user: UserCreateResponse = Depends(
        get_current_user
    ),
):
    response.delete_cookie(
        "fakesession"
    )  # Clear session data
    return {"message": "User logged out successfully"}
