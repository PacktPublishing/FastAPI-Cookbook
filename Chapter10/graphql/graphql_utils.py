import strawberry
from strawberry.fastapi import GraphQLRouter

from database import users_db


@strawberry.type
class User:
    username: str
    phone_number: str
    country: str


@strawberry.type
class Query:
    @strawberry.field
    def users(
        self, country: str | None
    ) -> list[User]:
        return [
            User(
                username=user.username,
                phone_number=user.phone_number,
                country=user.country,
            )
            for user in users_db
            if user.country == country
        ]


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
