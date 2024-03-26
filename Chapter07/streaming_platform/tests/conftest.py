from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.database import mongo_database
from app.main import app
from app.main_search import (
    get_elasticsearch_client as es_client,
)


def mock_find_songs_list():
    to_return = [
        {
            "_id": ObjectId("89abcdef0123456789abcdef"),
            "title": "Song 1",
            "artist": "Artist 1",
        },
        {
            "_id": ObjectId("23456789abcdef0123456789"),
            "title": "Song 2",
            "artist": "Artist 2",
        },
    ]
    song_list = MagicMock()
    print(song_list.id)
    song_list.to_list = AsyncMock(
        return_value=to_return
    )
    return song_list


@pytest.fixture
def mongo_db_mock():
    database = MagicMock()
    database.songs.insert_one = AsyncMock()

    song = {
        "_id": ObjectId("0123456789abcdef01234567"),
        "title": "Test Song",
        "artist": "Test Artist",
    }
    database.songs.find_one = AsyncMock(
        return_value=song
    )

    database.songs.find = MagicMock(
        return_value=mock_find_songs_list()
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
