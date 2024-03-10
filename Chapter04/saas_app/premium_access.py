from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from db_connection import get_session
from models import Role
from operations import add_user

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class ResponseCreateUser(BaseModel):
    message: Annotated[
        str, Field(default="user created")
    ]
    user: UserCreate


class UserCreateBody(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post(
    "/register/premium-user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        },
        status.HTTP_201_CREATED: {
            "description": "User created"
        },
    },
)
def register_premium_user(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreate]:
    user = add_user(
        session=session,
        **user.model_dump(),
        role=Role.premium,
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreate(
        username=user.username,
        email=user.email,
    )
    return {
        "message": "user created",
        "user": user_response,
    }


