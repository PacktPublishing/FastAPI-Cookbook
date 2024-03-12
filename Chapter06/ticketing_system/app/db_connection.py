from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
"sqlite+aiosqlite:///.database.db"
#    "sqlite+aiosqlite:///.database.db"
)


def get_engine():
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL, echo=True
    )


# sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)
