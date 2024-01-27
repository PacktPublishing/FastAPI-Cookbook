from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    mapped_column,
)

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    tweets = relationship("Tweet", back_populates="user")

    class Config:
        orm_mode = True


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="tweets")


Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
