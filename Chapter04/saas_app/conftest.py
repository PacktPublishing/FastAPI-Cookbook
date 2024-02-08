import pytest
from passlib.context import CryptContext
from sqlalchemy import create_engine, QueuePool
from sqlalchemy.orm import sessionmaker

from models import Base, User, Role, SessionLocal

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
    )

    Base.metadata.create_all(bind=engine)

    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    db_session = session_local()

    yield db_session

    db_session.close()


@pytest.fixture(scope="function")
def fill_database_session(session):
    (
        session.add(
            User(
                username="johndoe",
                email="johndoe@email.com",
                hashed_password=pwd_context.hash(
                    "pass1234"
                ),
                role=Role.basic,
            )
        ),
    )
    (
        session.add(
            User(
                username="chrissophia",
                email="chrissophia@email.com",
                hashed_password=pwd_context.hash(
                    "hardpass"
                ),
                role=Role.basic,
            )
        ),
    )
    (
        session.add(
            User(
                username="manucourtney",
                email="mcourtney@email.com",
                hashed_password=pwd_context.hash(
                    "harderpass"
                ),
                role=Role.premium,
            )
        ),
    )
    session.commit()
    yield session
