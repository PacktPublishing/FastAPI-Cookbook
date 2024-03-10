from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from db_connection import get_session
from models import Role
from security import decode_access_token, oauth2_scheme


class UserCreateResponseWithRole(BaseModel):
    username: str
    email: EmailStr
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


router = APIRouter()


@router.get(
    "/welcome/all-users",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def all_user_can_access(
    user: UserCreateResponseWithRole = Depends(
        get_current_user
    ),
):
    return {
        f"Hello {user.username}, welcome to your space"
    }


@router.get(
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
