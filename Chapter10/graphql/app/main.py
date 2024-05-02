import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Post:
    id: int
    title: str
    content: str


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    def posts(self) -> list[Post]:
        return [
            Post(
                id=1,
                title="First Post",
                content="Hello, World!",
            ),
            Post(
                id=2,
                title="Second Post",
                content="Hello, FastAPI!",
            )
        ]


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
