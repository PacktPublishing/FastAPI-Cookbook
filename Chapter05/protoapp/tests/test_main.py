import pytest
from httpx import AsyncClient

from protoapp.database import Item
from protoapp.main import app


@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as ac:
        response = await ac.get("/home")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_main_client(test_client):
    response = test_client.get("/home")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.integration
def test_client_can_add_read_the_item_from_database(
    test_client, db_session_test
):
    response = test_client.get("/item/1")
    assert response.status_code == 404

    response = test_client.post(
        "/item", json={"name": "ball", "color": "red"}
    )
    assert response.status_code == 201
    # Verify the user was added to the database
    item_id = response.json()
    item = (
        db_session_test.query(Item)
        .filter(Item.id == item_id)
        .first()
    )
    assert item is not None

    response = test_client.get("item/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "ball",
        "color": "red",
    }
