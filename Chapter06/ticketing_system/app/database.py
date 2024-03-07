from sqlalchemy import Column, Float, ForeignKey, Table
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
    event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id")
    )
    event: Mapped["Event | None"] = relationship(
        back_populates="tickets"
    )


class TicketDetails(Base):
    __tablename__ = "ticket_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id")
    )
    ticket: Mapped["Ticket"] = relationship(
        back_populates="details"
    )
    seat: Mapped[str | None]
    ticket_type: Mapped[str | None]


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="event"
    )
    sponsors: Mapped[list["Sponsor"]] = relationship(
        secondary="sponsorships",
        back_populates="events",
    )


class Sponsor(Base):
    __tablename__ = "sponsors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    events: Mapped[list["Event"]] = relationship(
        secondary="sponsorships",
        back_populates="sponsors",
    )


Sponsorship = Table(
    "sponsorships",
    Base.metadata,
    Column(
        "event_id",
        ForeignKey("events.id"),
        primary_key=True,
    ),
    Column(
        "sponsor_id",
        ForeignKey("sponsors.id"),
        primary_key=True,
    ),
    Column(
        "amount",
        Float,
        nullable=False,
        default=10,
    ),
)
