import csv
import os
from pathlib import Path
from unittest.mock import patch

import pytest

TEST_DATABASE_FILE = "test_tasks.csv"

TEST_TASKS_CSV = [
    {
        "id": "1",
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete",
    },
    {
        "id": "2",
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "Ongoing",
    },
]

TEST_TASKS = [
    {**task_json, "id": int(task_json["id"])}
    for task_json in TEST_TASKS_CSV
]


@pytest.fixture(autouse=True)
def create_test_database():
    database_file_location = str(
        Path(__file__).parent / TEST_DATABASE_FILE
    )
    with patch(
        "operations.DATABASE_FILENAME",
        database_file_location,
    ) as csv_test:
        with open(
            database_file_location, mode="w", newline=""
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "id",
                    "title",
                    "description",
                    "status",
                ],
            )
            writer.writeheader()
            writer.writerows(TEST_TASKS_CSV)
            print("")
        yield csv_test
        os.remove(database_file_location)
