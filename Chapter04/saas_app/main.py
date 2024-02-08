from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from models import Role, SessionLocal
from operations import add_user
from security import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    oauth2_scheme,
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI(title="Banking Application")


class UserCreateBody(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr


class ResponseCreateUser(BaseModel):
    message: Annotated[str, Field(default="user created")]
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
    user = add_user(session=session, **user.model_dump())
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


@app.post(
    "/register/premium-user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
)
def register_premium_user(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreateResponse]:
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
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password"
        }
    },
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get(
    "/users/me",
    response_model=UserCreateResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def read_user_me(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return UserCreateResponse(
        username=user.username, email=user.email
    )


class UserCreateResponseWithRole(UserCreateResponse):
    role: Role


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> UserCreateResponseWithRole:
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )

    return UserCreateResponseWithRole(
        username=user.username,
        email=user.email,
        role=user.role,
    )


def get_premium_user(
    current_user: UserCreateResponseWithRole = Depends(
        get_current_user
    ),
):
    if current_user.role != Role.premium:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return current_user


@app.get(
    "/welcome/all-users",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def get_basic_user_information(
    user: UserCreateResponseWithRole = Depends(
        get_current_user
    ),
):
    return {
        f"Hello {user.username}, welcome to your space"
    }


@app.get(
    "/welcome/premium-user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def get_premium_user_information(
    user: UserCreateResponseWithRole = Depends(
        get_premium_user
    ),
):
    return {
        f"Hello {user.username}, welcome to your premium space"
    }
