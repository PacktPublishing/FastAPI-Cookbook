from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    phone_number: str
    country: str


users_db: list[User] = [
    User(
        id=1,
        username="user1",
        phone_number="1234567890",
        country="USA",
    ),
    User(
        id=2,
        username="user2",
        phone_number="0987654321",
        country="Canada",
    ),
    User(
        id=3,
        username="user3",
        phone_number="9876543210",
        country="UK",
    ),
    User(
        id=4,
        username="user4",
        phone_number="5555555555",
        country="Mexico",
    ),
    User(
        id=5,
        username="user5",
        phone_number="9999999999",
        country="Brazil",
    ),
    User(
        id=6,
        username="user6",
        phone_number="1111111111",
        country="Germany",
    ),
    User(
        id=7,
        username="user7",
        phone_number="2222222222",
        country="France",
    ),
    User(
        id=8,
        username="user8",
        phone_number="3333333333",
        country="Italy",
    ),
    User(
        id=9,
        username="user9",
        phone_number="4444444444",
        country="Spain",
    ),
    User(
        id=10,
        username="user10",
        phone_number="5555555555",
        country="Portugal",
    ),
    User(
        id=11,
        username="user11",
        phone_number="6666666666",
        country="Russia",
    ),
    User(
        id=12,
        username="user12",
        phone_number="7777777777",
        country="China",
    ),
    User(
        id=13,
        username="user13",
        phone_number="8888888888",
        country="Japan",
    ),
    User(
        id=14,
        username="user14",
        phone_number="9999999999",
        country="India",
    ),
    User(
        id=15,
        username="user15",
        phone_number="0000000000",
        country="South Africa",
    ),
    User(
        id=16,
        username="user16",
        phone_number="1111111111",
        country="Egypt",
    ),
    User(
        id=17,
        username="user17",
        phone_number="2222222222",
        country="Nigeria",
    ),
    User(
        id=18,
        username="user18",
        phone_number="3333333333",
        country="Kenya",
    ),
    User(
        id=19,
        username="user19",
        phone_number="4444444444",
        country="New Zealand",
    ),
    User(
        id=20,
        username="user20",
        phone_number="0123456789",
        country="Australia",
    ),
]
