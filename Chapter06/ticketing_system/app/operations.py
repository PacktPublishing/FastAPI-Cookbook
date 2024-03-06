from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Ticket


async def get_ticket(
    db_session: AsyncSession, ticket_id: int
) -> Ticket:
    async with db_session as session:
        tickets = await session.execute(
            select(Ticket).filter(
                Ticket.id == ticket_id
            )
        )
        return tickets.scalars().first()


async def create_ticket(
    db_session: AsyncSession,
    show_name: str,
    user: str = None,
    price: float = None,
) -> int:
    async with db_session.begin():
        ticket = Ticket(
            show=show_name, user=user, price=price
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


async def update_ticket_price(
    db_session: AsyncSession,
    ticket_id: int,
    price: float,
) -> bool:
    async with db_session as session:
        result = await db_session.execute(
            update(Ticket)
            .where(Ticket.id == ticket_id)
            .values(price=price)
        )
        await session.commit()

        if result.rowcount == 0:
            return False
        return True
