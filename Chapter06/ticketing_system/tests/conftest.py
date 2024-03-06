import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.database import Base, Ticket
from app.main import app, get_db_session


@pytest.fixture
def db_engine_test():
    engine = create_async_engine(
        "sqlite+aiosqlite:///.test_database.db"
    )
    return engine


@pytest.fixture
async def db_session_test(
    db_engine_test,
):
    TestingAsynSessionLocal = sessionmaker(
        bind=db_engine_test, class_=AsyncSession
    )
    async with db_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with TestingAsynSessionLocal() as session:
            yield session

        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def fill_database_with_tickets(db_session_test):
    tickets = [
        Ticket(show="The Rolling Stones Concert")
        for _ in range(10)
    ]
    async with db_session_test.begin():
        db_session_test.add_all(tickets)
        await db_session_test.commit()


@pytest.fixture
async def add_special_ticket(db_session_test):
    ticket = Ticket(id=1234, show="Special Show")
    async with db_session_test.begin():
        db_session_test.add(ticket)
        await db_session_test.commit()


@pytest.fixture
def test_client(db_session_test):
    client = TestClient(app=app)
    app.dependency_overrides[get_db_session] = (
        lambda: db_session_test
    )
    return client
