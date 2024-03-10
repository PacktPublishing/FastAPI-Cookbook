from enum import Enum
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"


@lru_cache
def get_engine():
    return create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    basic = "basic"
    premium = "premium"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    username: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(
        default=Role.basic
    )
    totp_secret: Mapped[str] = mapped_column(
        nullable=True
    )


def get_session():
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine(),
    )
    try:
        session = Session()
        yield session
    finally:
        session.close()
