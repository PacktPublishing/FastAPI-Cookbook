from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
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


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(nullable=True)
    show: Mapped[str | None]
    user: Mapped[str | None]
    sold: Mapped[bool] = mapped_column(default=False)
    details: Mapped["TicketDetails"] = relationship(
        back_populates="ticket"
    )


class TicketDetails(Base):
    __tablename__ = "ticket_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id")
    )
    ticket: Mapped["Ticket"] = relationship(
        "Ticket", back_populates="details"
    )
    seat: Mapped[str | None]
    ticket_type: Mapped[str | None]
