GITHUB_CLIENT_ID = "fbbf3b6dc518fbc16347"
GITHUB_CLIENT_SECRET = (
    "aeae722bf334023e9b8e7a94b950fd776f8bb9a5"
)
GITHUB_REDIRECT_URI = (
    "http://localhost:8000/github/auth/token"
)


import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from sqlalchemy.orm import Session

from models import User, get_session
from operations import get_user


def resolve_github_token(
    access_token: str = Depends(OAuth2()),
    session: Session = Depends(get_session),
) -> User:
    user_response = httpx.get(
        "https://api.github.com/user",
        headers={"Authorization": access_token},
    ).json()
    username = user_response.get("login", " ")
    user = get_user(session, username)
    if not user:
        email = user_response.get("email", " ")
        user = get_user(session, email)
    # Process user_response to log
    # the user in or create a new account
    if not user:
        raise HTTPException(
            status_code=403, detail="Token not valid"
        )
    return user
