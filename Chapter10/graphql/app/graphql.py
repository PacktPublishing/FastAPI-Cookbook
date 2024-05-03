import strawberry
from strawberry.fastapi import GraphQLRouter

from app.database import users_db


@strawberry.type
class User:
    id: int
    username: str
    phone_number: str
    country: str


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        user = users_db[0]
        return [
            User(
                id=user.id,
                username=user.username,
                phone_number=user.phone_number,
                country=user.country,
            ),
        ]


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
