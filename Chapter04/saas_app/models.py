from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum

SQLALCHEMY_DATABASE_URL = f"sqlite:///database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

Base = declarative_base()


class Role(str, Enum):
    basic = "basic"
    premium = "premium"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(Role))


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
