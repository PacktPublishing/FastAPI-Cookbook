from fastapi import APIRouter

from app.db_connection import es_client

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


def get_elasticsearch_client():
    return es_client
