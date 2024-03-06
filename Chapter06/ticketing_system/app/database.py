from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

SQLALCHEMY_DATABASE_URL = (
    "sqlite+aiosqlite:///.database.db"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=True)
    show = Column(String)
    user = Column(String, nullable=True)
