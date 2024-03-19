from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app, mongo_database
from app.main_search import (
    get_elasticsearch_client as es_client,
)


async def songs():
    yield {
        "_id": "1",
        "title": "Song 1",
        "artist": "Artist 1",
    }
    yield {
        "_id": "2",
        "title": "Song 2",
        "artist": "Artist 2",
    }


@pytest.fixture
def mongo_db_mock():
    database = MagicMock()
    database.songs.insert_one = AsyncMock()

    song_id = "123"
    song = {
        "_id": song_id,
        "title": "Test Song",
        "artist": "Test Artist",
    }
    database.songs.find_one = AsyncMock(
        return_value=song
    )

    database.songs.find = MagicMock(
        # return_value=songs()
        return_value=songs()
    )

    result_mock = MagicMock()
    result_mock.modified_count = 1
    database.songs.update_one = AsyncMock(
        return_value=result_mock
    )

    result_mock.deleted_count = 1
    database.songs.delete_one = AsyncMock(
        return_value=result_mock
    )

    return database


@pytest.fixture
def es_client_mock():
    client = MagicMock()
    client.index = AsyncMock()
    client.search = AsyncMock()
    return client


@pytest.fixture
def test_client(mongo_db_mock, es_client_mock):
    client = TestClient(app)
    client.app.dependency_overrides[mongo_database] = (
        lambda: mongo_db_mock
    )
    client.app.dependency_overrides[es_client] = (
        lambda: es_client_mock
    )

    return client
