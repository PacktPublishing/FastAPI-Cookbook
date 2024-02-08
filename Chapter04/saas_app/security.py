from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import User
from operations import get_user

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    token: str, session: Session
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
    user = get_user(session, username)
    return user
