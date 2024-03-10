import pytest
from passlib.context import CryptContext
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Role, User

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

    session_local = sessionmaker(engine)

    db_session = session_local()

    Base.metadata.create_all(bind=engine)

    yield db_session

    Base.metadata.drop_all(bind=engine)

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
