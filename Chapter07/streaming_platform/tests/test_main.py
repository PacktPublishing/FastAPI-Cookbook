from bson import ObjectId


def test_add_song(test_client, mongo_db_mock):
    song = {
        "title": "Test Song",
        "artist": "Test Artist",
    }

    response = test_client.post("/song", json=song)

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Song added successfully"
    )
    mongo_db_mock.songs.insert_one.assert_called_once_with(
        song
    )


def test_get_song(test_client, mongo_db_mock):
    response = test_client.get(
        "/song/0123456789abcdef01234567"
    )

    assert response.status_code == 200
    assert response.json() == {
        "_id": "0123456789abcdef01234567",
        "title": "Test Song",
        "artist": "Test Artist",
    }
    mongo_db_mock.songs.find_one.assert_called_once_with(
        {"_id": ObjectId("0123456789abcdef01234567")}
    )


def test_get_songs(test_client, mongo_db_mock):
    response = test_client.get("/songs")

    assert response.status_code == 200
    assert response.json() == [
        {
            "_id": "89abcdef0123456789abcdef",
            "title": "Song 1",
            "artist": "Artist 1",
        },
        {
            "_id": "23456789abcdef0123456789",
            "title": "Song 2",
            "artist": "Artist 2",
        },
    ]
    mongo_db_mock.songs.find.assert_called_once()


def test_update_song(test_client, mongo_db_mock):
    song_id = "0123456789abcdef01234567"
    updated_song = {
        "title": "Updated Song",
        "artist": "Updated Artist",
    }

    response = test_client.put(
        f"/song/{song_id}", json=updated_song
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Song updated successfully"
    }

    mongo_db_mock.songs.update_one.assert_called_once_with(
        {"_id": ObjectId(song_id)},
        {"$set": updated_song},
    )


def test_delete_song(test_client, mongo_db_mock):
    response = test_client.delete(
        "/song/0123456789abcdef01234567"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Song deleted successfully"
    }
    mongo_db_mock.songs.delete_one.assert_called_once_with(
        {"_id": ObjectId("0123456789abcdef01234567")}
    )
