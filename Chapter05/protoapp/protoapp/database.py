from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

logger = logging.getLogger(__name__)


Base = declarative_base()

DATABASE_URL = "sqlite:///./production.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)


logger.debug("Binding the engine to the database")
Base.metadata.create_all(bind=engine)
