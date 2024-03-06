from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Base, engine
from app.operations import (
    create_ticket,
    delete_ticket,
    get_all_tickets_for_show,
    get_ticket,
    update_ticket_price,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield


app = FastAPI(lifespan=lifespan)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/ticket/{ticket_id}")
async def read_ticket(
    ticket_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    ticket = await get_ticket(db_session, ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return ticket


class TicketRequest(BaseModel):
    price: float | None
    show: str | None
    user: str | None = None


@app.post("/ticket", response_model=dict[str, int])
async def post_ticket(
    ticket: TicketRequest,
    db_session: AsyncSession = Depends(get_db_session),
):
    ticket_id = await create_ticket(
        db_session,
        ticket.show,
        ticket.user,
        ticket.price,
    )
    return {"ticket_id": ticket_id}


@app.put("/ticket/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    price: float,
    db_session: AsyncSession = Depends(get_db_session),
):
    updated = await update_ticket_price(
        db_session, ticket_id, price
    )
    if not updated:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return {"detail": "Price updated"}


@app.delete("/ticket/{ticket_id}")
async def delete_ticket_route(
    ticket_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    ticket = await delete_ticket(db_session, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return {"detail": "Ticket removed"}

class TicketResponse(TicketRequest):
    id: int

@app.get(
    "/tickets/{show}",
    response_model=list[TicketResponse],
)
async def get_tickets_for_show(
    show: str,
    db_session: AsyncSession = Depends(get_db_session),
):
    tickets = await get_all_tickets_for_show(
        db_session, show
    )
    return tickets
