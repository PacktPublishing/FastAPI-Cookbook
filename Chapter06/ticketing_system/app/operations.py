from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.database import Ticket, TicketDetails


async def get_ticket(
    db_session: AsyncSession, ticket_id: int
) -> Ticket:
    query = (
        select(Ticket)
        .options(joinedload(Ticket.details))
        .where(Ticket.id == ticket_id)
    )
    async with db_session as session:
        tickets = await session.execute(query)
        return tickets.scalars().first()


async def create_ticket(
    db_session: AsyncSession,
    show_name: str,
    user: str = None,
    price: float = None,
) -> int:
    async with db_session.begin():
        ticket = Ticket(
            show=show_name,
            user=user,
            price=price,
            details=TicketDetails(),
        )
        db_session.add(ticket)
        await db_session.flush()
        ticket_id = ticket.id
        await db_session.commit()
    return ticket_id


async def get_all_tickets_for_show(
    db_session: AsyncSession, show: str
) -> list[Ticket]:
    async with db_session as session:
        result = await session.execute(
            select(Ticket).filter(Ticket.show == show)
        )
        tickets = result.scalars().all()
    return tickets


async def delete_ticket(
    db_session: AsyncSession, ticket_id
) -> bool:
    async with db_session as session:
        tickets_removed = await session.execute(
            delete(Ticket).where(Ticket.id == ticket_id)
        )
        await session.commit()

        if tickets_removed.rowcount == 0:
            return False
        return True


async def update_ticket(
    db_session: AsyncSession,
    ticket_id: int,
    update_ticket_dict: dict,
) -> bool:
    ticket_query = update(Ticket).where(
        Ticket.id == ticket_id
    )
    if "price" in update_ticket_dict.keys():
        ticket_query = ticket_query.values(
            price=update_ticket_dict["price"]
        )
        result = await db_session.execute(ticket_query)
        if result.rowcount == 0:
            return False

    if "details" in update_ticket_dict.keys():
        # update ticket details
        details = update_ticket_dict["details"]

        details_query = update(TicketDetails).where(
            TicketDetails.ticket_id == ticket_id
        )

        if "seat" in details.keys():
            details_query = details_query.values(
                seat=details["seat"]
            )
        if "ticket_type" in details.keys():
            details_query = details_query.values(
                ticket_type=details["ticket_type"]
            )

        result = await db_session.execute(details_query)
        if result.rowcount == 0:
            return False

    return True
