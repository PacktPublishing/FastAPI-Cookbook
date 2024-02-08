from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import User
from passlib.context import CryptContext
from email_validator import (
    validate_email,
    EmailNotValidError,
)
from models import Role

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def add_user(
    session: Session,
    username: str,
    password: str,
    email: str,
    role: Role = Role.basic,
) -> User | None:
    db_user = (
        session.query(User)
        .filter(
            or_(
                User.username == username,
                User.email == email,
            )
        )
        .first()
    )
    if db_user:
        return
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(
    session: Session, username_or_email: str
) -> User | None:
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    user = (
        session.query(User)
        .filter(query_filter == username_or_email)
        .first()
    )
    return user
