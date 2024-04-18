import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.database import (
    Base,
    Event,
    Sponsor,
    Sponsorship,
    Ticket,
    TicketDetails,
)
from app.db_connection import get_db_session
from app.main import app


@pytest.fixture
def db_engine_test():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
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
    await db_engine_test.dispose()


@pytest.fixture
async def second_session_test(
    db_engine_test,
):
    TestingAsynSessionLocal = sessionmaker(
        bind=db_engine_test, class_=AsyncSession
    )
    async with TestingAsynSessionLocal() as session:
        yield session


@pytest.fixture
async def third_session_test(
    db_engine_test,
):
    TestingAsynSessionLocal = sessionmaker(
        bind=db_engine_test, class_=AsyncSession
    )
    async with TestingAsynSessionLocal() as session:
        yield session


@pytest.fixture
async def fourth_session_test(
    db_engine_test,
):
    TestingAsynSessionLocal = sessionmaker(
        bind=db_engine_test, class_=AsyncSession
    )
    async with TestingAsynSessionLocal() as session:
        yield session


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
    ticket = Ticket(
        id=1234,
        show="Special Show",
        details=TicketDetails(),
    )
    async with db_session_test.begin():
        db_session_test.add(ticket)
        await db_session_test.commit()


@pytest.fixture
async def add_special_sold_ticket(db_session_test):
    ticket = Ticket(
        id=1234,
        show="Special Show",
        details=TicketDetails(),
        sold=True,
        user="John Doe",
    )
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


@pytest.fixture
async def add_event_and_sponsor(db_session_test):
    event = Event(name="The Rolling Stones Concert")
    sponsor = Sponsor(name="Live Nation")
    async with db_session_test.begin():
        db_session_test.add(event)
        db_session_test.add(sponsor)
        await db_session_test.commit()


@pytest.fixture
async def add_event_with_tickets(db_session_test):
    event = Event(name="The Rolling Stones Concert")
    users = [
        "John Doe",
        "Jane Doe",
        "Foo Bar",
        "Bar Foo",
    ]
    tickets = [
        Ticket(
            show="The Rolling Stones Concert",
            event_id=1,
            price=100,
            user=users[j] if j < 3 else None,
            sold=True if j < 3 else False,
        )
        for j in range(10)
    ]
    async with db_session_test.begin():
        db_session_test.add(event)
        await db_session_test.flush()
        db_session_test.add_all(tickets)
        await db_session_test.commit()


@pytest.fixture
async def add_event_and_sponsor_and_sponsorship(
    db_session_test, add_event_and_sponsor
):
    sponsorship = Sponsorship(
        event_id=1, sponsor_id=1, amount=10
    )
    async with db_session_test.begin():
        db_session_test.add(sponsorship)
        await db_session_test.commit()


@pytest.fixture
async def add_sponsors_for_event(
    db_session_test,
):
    event = Event(name="The Rolling Stones Concert")
    sponsors = [
        Sponsor(name="Live Nation"),
        Sponsor(name="Ticketmaster"),
        Sponsor(name="Spotify"),
    ]

    async with db_session_test.begin():
        db_session_test.add(event)
        db_session_test.add_all(sponsors)
        await db_session_test.flush()
        for k, sponsor in enumerate(sponsors):
            db_session_test.add(
                Sponsorship(
                    event_id=event.id,
                    sponsor_id=sponsor.id,
                    amount=10 + k * 20,
                )
            )

        await db_session_test.commit()
