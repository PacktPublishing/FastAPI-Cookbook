from datetime import date

from fastapi.testclient import TestClient

from app.dependencies import time_range
from app.main import app


def test_get_v1_trips_endpoint():
    client = TestClient(app)
    app.dependency_overrides[time_range] = lambda: (
        date.fromisoformat("2024-02-01"),
        None,
    )
    response = client.get("/v1/trips")
    assert (
        response.json()
        == "Request trips from 2024-02-01"
    )
