from typing import Optional

from database import user_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator

app = FastAPI()


class Tweet(BaseModel):
    content: str
    hashtags: list[str]


class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int]
    tweets: list[Tweet]

    @validator
    def validate_age(cls, value):
        if value < 18 or value > 100:
            raise ValueError(
                "Age must be between 18 and 100"
            )
        return value


class UserResponse(User):
    id: str


@app.get("/users")
async def read_users():
    users = []
    async for user in user_collection.find():
        users.append(User(**user))
    return users


@app.post("/user", response_model=UserResponse)
async def create_user(user: User):
    result = await user_collection.insert_one(
        user.model_dump()
    )
    user_response = UserResponse(
        id=str(result.inserted_id), **user.model_dump()
    )
    return user_response


@app.get("/user")
async def get_user(user_id: str):
    db_user = await user_collection.find_one(
        {"_id": user_id}
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    return db_user


@app.post("/user/{user_id}")
async def update_user(
    user_id: str,
    user: User,
):
    db_user = await user_collection.update_one(
        {"_id": user_id}, {"$set": user}
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    return db_user


@app.delete("/user")
async def delete_user(user_id: str):
    db_user = await user_collection.delete_one(
        {"_id": user_id}
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )

    return {"detail": "User deleted"}
