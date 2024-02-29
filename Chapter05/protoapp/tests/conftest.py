import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from protoapp.database import Base
from protoapp.main import app, get_db_session


@pytest.fixture(scope="function")
def db_session_test():
    engine = create_engine("sqlite:///./test_test.db")
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    Base.metadata.create_all(
        bind=engine
    )  # Create tables
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(db_session_test):
    client = TestClient(app)
    app.dependency_overrides[get_db_session] = (
        lambda: db_session_test
    )

    return client
