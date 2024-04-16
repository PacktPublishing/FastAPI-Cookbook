from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)

from database import user_collection

app = FastAPI()


class Tweet(BaseModel):
    content: str
    hashtags: list[str]


class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    tweets: list[Tweet] | None = None

    @field_validator("age")
    def validate_age(cls, value):
        if value < 18 or value > 100:
            raise ValueError(
                "Age must be between 18 and 100"
            )
        return value


@app.get("/users")
def read_users() -> list[User]:
    return [user for user in user_collection.find()]


class UserResponse(User):
    id: str


@app.post("/user")
def create_user(user: User) -> UserResponse:
    result = user_collection.insert_one(
        user.model_dump(exclude_none=True)
    )
    user_response = UserResponse(
        id=str(result.inserted_id), **user.model_dump()
    )
    return user_response


@app.get("/user")
def get_user(user_id: str) -> UserResponse:
    db_user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
            if ObjectId.is_valid(user_id)
            else None
        }
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    db_user["id"] = str(db_user["_id"])
    return db_user
