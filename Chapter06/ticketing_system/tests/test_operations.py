import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.database import Event, Sponsorship, Ticket
from app.operations import (
    add_sponsor_to_event,
    create_event,
    create_ticket,
    delete_ticket,
    get_all_tickets_for_show,
    get_event,
    get_event_sponsorships_with_amount,
    get_ticket,
    sell_ticket_to_user,
    update_ticket,
    update_ticket_price,
)


async def assert_tickets_table_is_empty(
    db_session: AsyncSession,
):
    async with db_session as session:
        result = await session.execute(select(Ticket))
    assert result.all() == []


async def test_create_ticket_for_rolling_stones(
    db_session_test,
):
    await assert_tickets_table_is_empty(db_session_test)

    ticket_id = await create_ticket(
        db_session_test, "Rolling Stones"
    )

    async with db_session_test as session:
        result = await session.execute(select(Ticket))
        items = result.scalars().all()

    assert ticket_id == 1
    assert len(items) == 1
    assert items[0].show == "Rolling Stones"


async def test_read_tickets_for_rolling_stone_show(
    fill_database_with_tickets, db_session_test
):
    tickets = await get_all_tickets_for_show(
        db_session_test, "The Rolling Stones Concert"
    )
    assert len(tickets) == 10


async def test_get_ticket(
    add_special_ticket, db_session_test
):
    ticket = await get_ticket(db_session_test, 1234)

    assert ticket.id == 1234
    assert ticket.show == "Special Show"


async def test_delete_ticket(
    add_special_ticket, db_session_test
):
    assert (
        await delete_ticket(db_session_test, 5555)
        is False
    )  # non existing ticket

    assert (
        await delete_ticket(db_session_test, 1234)
        is True
    )  # existing ticket

    await assert_tickets_table_is_empty(db_session_test)


async def test_update_ticket_price(
    add_special_ticket, db_session_test
):
    await update_ticket_price(
        db_session_test,
        ticket_id=1234,
        new_price=100,
    )
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.price == 100

    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"price": None},
    )

    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.price is None


async def test_update_ticket_details(
    add_special_ticket, db_session_test
):
    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"details": {"seat": "A1"}},
    )
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.details.seat == "A1"

    await update_ticket(
        db_session_test,
        ticket_id=1234,
        update_ticket_dict={"details": {"seat": None}},
    )

    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.details.seat is None


async def test_update_ticket_sell_to_user(
    add_special_ticket, db_session_test
):
    await sell_ticket_to_user(
        db_session_test,
        ticket_id=1234,
        user="John",
    )
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.user == "John"
    assert ticket.sold is True


async def test_ticket_cannot_sell_sold_ticket(
    add_special_sold_ticket, db_session_test
):
    result = await sell_ticket_to_user(
        db_session_test,
        ticket_id=1234,
        user="Jake Fake",
    )

    assert result is False
    ticket = await get_ticket(db_session_test, 1234)
    assert ticket.sold is True
    assert ticket.user == "John Doe"


async def test_create_event_without_tickets(
    db_session_test,
):
    await create_event(db_session_test, "Event 1")
    async with db_session_test as session:
        result = await session.execute(
            select(Event).options(
                joinedload(Event.tickets)
            )
        )
        event = result.scalars().first()
    assert event.name == "Event 1"
    assert len(event.tickets) == 0


async def test_create_event_with_10_tickets(
    db_session_test,
):
    await create_event(db_session_test, "Event 2", 10)
    async with db_session_test as session:
        result = await session.execute(
            select(Event).options(
                joinedload(Event.tickets)
            )
        )
        event = result.scalars().first()

    assert event.name == "Event 2"
    assert len(event.tickets) == 10
    assert event.tickets[0].show == "Event 2"


async def test_register_sponsorship(
    add_event_and_sponsor, db_session_test
):
    await add_sponsor_to_event(
        db_session_test, 1, 1, 100
    )
    async with db_session_test as session:
        result = await session.execute(
            select(Event).options(
                joinedload(Event.sponsors)
            )
        )

        event = result.scalars().first()

    assert event.sponsors[0].name == "Live Nation"


async def test_update_sponsorship_amount(
    add_event_and_sponsor_and_sponsorship,
    db_session_test,
):
    await add_sponsor_to_event(
        db_session_test, 1, 1, 200
    )
    async with db_session_test as session:
        result = await session.execute(
            select(Sponsorship)
        )

        sponsorship = result.scalars().first()

    assert sponsorship.amount == 210


async def test_get_event_with_sponsors(
    add_event_and_sponsor_and_sponsorship,
    db_session_test,
):
    event = await get_event(db_session_test, 1)
    assert event.sponsors[0].name == "Live Nation"


async def test_concurrent_ticket_sales(
    add_special_ticket,
    db_session_test,
    second_session_test,
):
    result = await asyncio.gather(
        sell_ticket_to_user(
            db_session_test, 1234, "Jake Fake"
        ),
        sell_ticket_to_user(
            second_session_test, 1234, "John Doe"
        ),
    )

    assert result in (
        [True, False],
        [False, True],
    )  # only one of the sales should be successful

    ticket = await get_ticket(db_session_test, 1234)

    # assert that the user who bought the ticket
    # correspond to the successful sale
    if result[0]:
        assert ticket.user == "Jake Fake"
    else:
        assert ticket.user == "John Doe"


async def test_get_event_sponsorships_with_amount(
    add_sponsors_for_event, db_session_test
):
    result = await get_event_sponsorships_with_amount(
        db_session=db_session_test, event_id=1
    )
    print(result)
    assert result == [
        ("Spotify", 50.0),
        ("Ticketmaster", 30.0),
        ("Live Nation", 10.0),
    ]
