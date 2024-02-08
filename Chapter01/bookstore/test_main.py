from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_book_by_id():
    response = client.get("/books/9999")

    assert response.status_code == 200

    assert response.json() == {
        "book_id": 9999,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
    }
