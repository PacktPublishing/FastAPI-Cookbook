import pytest
from fastapi.testclient import TestClient

from db_connection import get_session
from main import app


@pytest.fixture
def client(session):
    app.dependency_overrides |= {
        get_session: lambda: session
    }
    testclient = TestClient(app)
    return testclient


def test_endpoint_add_basic_user(client):
    user = {
        "username": "lyampayet",
        "password": "difficultpassword",
        "email": "lyampayet@email.com",
    }

    response = client.post("/register/user", json=user)
    assert response.status_code == 201
    assert response.json() == {
        "message": "user created",
        "user": {
            "username": "lyampayet",
            "email": "lyampayet@email.com",
        },
    }


def test_endpoint_add_user_conflict_existing_user(
    client, fill_database_session
):
    user = {
        "username": "johndoe",
        "password": "strongpassword",
        "email": "johndoe@email.com",
    }
    response = client.post("/register/user", json=user)
    assert response.status_code == 409
    assert response.json() == {
        "detail": "username or email already exists"
    }


def test_endpoint_add_premium_user(client):
    user = {
        "username": "mariorossi",
        "password": "difficultpassword",
        "email": "mariorossi@email.com",
    }

    response = client.post("/register/user", json=user)
    assert response.status_code == 201
    assert response.json() == {
        "message": "user created",
        "user": {
            "username": "mariorossi",
            "email": "mariorossi@email.com",
        },
    }


