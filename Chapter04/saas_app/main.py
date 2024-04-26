from contextlib import asynccontextmanager

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

import api_key
import github_login
import mfa
import premium_access
import rbac
import security
import user_session
from db_connection import get_engine, get_session
from models import Base
from operations import add_user
from responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse,
)
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
app.include_router(rbac.router)
app.include_router(github_login.router)
app.include_router(mfa.router)
app.include_router(user_session.router)
app.include_router(api_key.router)


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
