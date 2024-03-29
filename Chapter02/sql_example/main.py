from fastapi import (
    Body,
    Depends,
    FastAPI,
    HTTPException,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, Tweet, User

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserBody(BaseModel):
    name: str
    email: str


@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/user")
def add_new_user(
    user: UserBody, db: Session = Depends(get_db)
):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user


@app.get("/user")
def get_user(
    user_id: int, db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )

    return user


@app.post("/user/{user_id}")
def update_user(
    user_id: int,
    user: UserBody,
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/user")
def delete_user(
    user_id: int, db: Session = Depends(get_db)
):
    db_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}


@app.post("/tweet/user/{user_id}")
def publish_tweet(
    user_id: int,
    tweet_content: str = Body(...),
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="User not found"
        )

    tweet = Tweet(
        content=tweet_content, user_id=user_id
    )
    db.add(tweet)
    db.commit()

    return {"detail": "tweet published"}


@app.get("/tweets/user/{user_id}")
def get_posts_of_user(
    user_id: int, db: Session = Depends(get_db)
):
    tweets = (
        db.query(Tweet)
        .filter(Tweet.user_id == user_id)
        .all()
    )
    return [tweet.content for tweet in tweets]
