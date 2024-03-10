from contextlib import (
    asynccontextmanager,
    contextmanager,
)
from typing import Annotated

import httpx
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from models import Base, Role, get_engine, get_session
from operations import add_user, get_user
from security import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    oauth2_scheme,
)
from third_party_login import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
    resolve_github_token,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(
    title="Saas application", lifespan=lifespan
)


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
def all_basic_user_can_access(
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
def only_premium_user_can_access(
    user: UserCreateResponseWithRole = Depends(
        get_premium_user
    ),
):
    return {
        f"Hello {user.username}, "
        "welcome to your premium space"
    }


router = APIRouter()


@router.get("/auth/url")
def github_login():
    return {
        "auth_url": "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
    }


@router.get(
    "/auth/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not registered"
        }
    },
)
async def github_callback(code: str):
    token_response = httpx.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={"Accept": "application/json"},
    ).json()
    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="User not registered",
        )
    token_type = token_response.get(
        "token_type", "bearer"
    )

    return {
        "access_token": access_token,
        "token_type": token_type,
    }


@router.get(
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


app.include_router(router, prefix="/github")


import pyotp

from mfa import generate_totp_secret, generate_totp_uri


@app.post("/user/enable-mfa")
def enable_mfa(
    user: UserCreateResponse = Depends(
        get_current_user
    ),
    db_session: Session = Depends(get_session),
):
    secret = generate_totp_secret()
    db_user = get_user(db_session, user.username)
    db_user.totp_secret = secret
    db_session.add(db_user)
    db_session.commit()
    totp_uri = generate_totp_uri(secret, user.email)

    # Return the TOTP URI
    # for QR code generation in the frontend
    return {
        "totp_uri": totp_uri,
        "secret_numbers": pyotp.TOTP(secret).now(),
    }


@app.post("/verify-totp")
def verify_totp(
    code: str,
    username: str,
    session: Session = Depends(get_session),
):
    user = get_user(session, username)
    if not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not activated",
        )

    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP token",
        )
    # Proceed with granting access
    # or performing the sensitive operation
    return {
        "message": "TOTP token verified successfully"
    }


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
    return {"message": "User logged out successfully"}
