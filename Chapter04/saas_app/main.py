from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

import github_login
import premium_access
import security
import mfa

from db_connection import get_engine, get_session
from models import Base
from operations import add_user, get_user
from rabc import get_current_user
from third_party_login import resolve_github_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(
    title="Saas application", lifespan=lifespan
)

app.include_router(security.router)
app.include_router(premium_access.router)
app.include_router(github_login.router)
app.include_router(mfa.router)


class UserCreateBody(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr


class ResponseCreateUser(BaseModel):
    message: Annotated[
        str, Field(default="user created")
    ]
    user: UserCreateResponse


@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
)
def register(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreateResponse]:
    user = add_user(
        session=session, **user.model_dump()
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }


@app.get(
    "/home",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "token not valid"
        }
    },
)
def homepage(
    user: UserCreateResponse = Depends(
        resolve_github_token
    ),
):
    return {"message": f"logged in {user.username} !"}





from api_key import get_api_key


@app.get("/secure-data")
async def get_secure_data(
    api_key: str = Depends(get_api_key),
):
    return {"message": "Access to secure data granted"}


from fastapi import Response


@app.post("/login")
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


@app.post("/logout")
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
