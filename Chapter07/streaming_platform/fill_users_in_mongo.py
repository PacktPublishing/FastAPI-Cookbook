import asyncio
from datetime import datetime

from app.db_connection import mongo_client

db = mongo_client.beat_streaming


users = [
    {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "year_of_birth": 1990,
        "country": "USA",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-01-01"
                ),
                "amount": 10,
            },
            {
                "action": "unscription",
                "date": datetime.fromisoformat(
                    "2021-05-01"
                ),
            },
        ],
        "consent_to_share_data": True,
    },
    {
        "name": "Alice Johnson",
        "email": "alicejohnson@email.com",
        "year_of_birth": 1995,
        "country": "UK",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-03-01"
                ),
                "amount": 10,
            },
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-05-02"
                ),
                "amount": 20,
            },
        ],
        "consent_to_share_data": True,
    },
    {
        "name": "Bob Williams",
        "email": "bobwilliams@email.com",
        "year_of_birth": 1988,
        "country": "Australia",
        "actions": [
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-06-02"
                ),
                "amount": 20,
            },
            {
                "action": "unscription",
                "date": datetime.fromisoformat(
                    "2021-08-01"
                ),
            },
        ],
        "consent_to_share_data": False,
    },
    {
        "name": "Emma Davis",
        "email": "emmadavis@email.com",
        "year_of_birth": 1992,
        "country": "Germany",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-05-01"
                ),
                "amount": 10,
            },
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-07-02"
                ),
                "amount": 20,
            },
            {
                "action": "unscription",
                "date": datetime.fromisoformat(
                    "2021-09-01"
                ),
            },
        ],
        "consent_to_share_data": True,
    },
    {
        "name": "Michael Johnson",
        "email": "michaeljohnson@email.com",
        "year_of_birth": 1980,
        "country": "USA",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-06-01"
                ),
                "amount": 10,
            },
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-08-02"
                ),
                "amount": 20,
            },
            {
                "action": "unscription",
                "date": "2021-10-01",
            },
        ],
        "consent_to_share_data": False,
    },
    {
        "name": "Sophia Brown",
        "email": "sophiabrown@email.com",
        "year_of_birth": 1998,
        "country": "Canada",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-07-01"
                ),
                "amount": 10,
            },
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-09-02"
                ),
                "amount": 20,
            },
            {
                "action": "unscription",
                "date": "2021-11-01",
            },
        ],
        "consent_to_share_data": True,
    },
    {
        "name": "Daniel Wilson",
        "email": "danielwilson@email.com",
        "year_of_birth": 1987,
        "country": "UK",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-08-01"
                ),
                "amount": 10,
            },
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2021-10-02"
                ),
                "amount": 20,
            },
            {
                "action": "unscription",
                "date": "2021-12-01",
            },
        ],
    },
    {
        "name": "Olivia Martinez",
        "email": "oliviamartinez@email.com",
        "year_of_birth": 1993,
        "country": "Australia",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-09-01"
                ),
                "amount": 10,
            },
        ],
        "consent_to_share_data": True,
    },
    {
        "name": "William Taylor",
        "email": "williamtaylor@email.com",
        "year_of_birth": 1983,
        "country": "Germany",
        "actions": [
            {
                "action": "basic subscription",
                "date": datetime.fromisoformat(
                    "2021-10-01"
                ),
                "amount": 10,
            },
        ],
    },
    {
        "name": "Emily Anderson",
        "email": "emilyanderson@email.com",
        "year_of_birth": 1996,
        "country": "USA",
        "actions": [
            {
                "action": "premium subscription",
                "date": datetime.fromisoformat(
                    "2022-01-02"
                ),
                "amount": 20,
            },
        ],
        "consent_to_share_data": True,
    },
]


async def add_users():
    await db.users.insert_many(users)


if __name__ == "__main__":
    asyncio.run(add_users())
