from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db_connection import get_session
from models import User
from operations import get_user, pwd_context


def authenticate_user(
    session: Session,
    username_or_email: str,
    password: str,
) -> User | None:
    user = get_user(session, username_or_email)

    if not user or not pwd_context.verify(
        password, user.hashed_password
    ):
        return
    return user


SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(
    token: str, db_session: Session
) -> User | None:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user = get_user(db_session, username)
    return user


router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password"
        }
    },
)
def get_user_access_token(
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/users/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        },
        status.HTTP_200_OK: {
            "description": "username authorized"
        },
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
    return {
        "description": f"{user.username} authorized",
    }
