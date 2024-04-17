import json
import logging

from elasticsearch import BadRequestError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from app.db_connection import es_client, redis_client
from app.es_queries import (
    top_ten_artists_query,
    top_ten_songs_query,
)

logger = logging.getLogger("uvicorn")


router = APIRouter(
    prefix="/search",
    tags=["search"],
)


def get_elasticsearch_client():
    return es_client


def get_redis_client():
    return redis_client


@router.get("/top/ten/artists/{country}")
async def top_ten_artist_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
    redis_client=Depends(get_redis_client),
):
    cache_key = f"top_ten_artists_{country}"

    cached_data = await redis_client.get(cache_key)
    if cached_data:
        logger.info(
            f"Returning cached data for {country}"
        )
        return json.loads(cached_data)

    logger.info(
        f"Getting top ten artists for {country}"
    )
    try:
        response = await es_client.search(
            **top_ten_artists_query(country)
        )
    except BadRequestError as e:
        logger.error(e)

        raise HTTPException(
            status_code=400,
            detail="Invalid country",
        )

    artists = [
        {
            "artist": record.get("key"),
            "views": record.get("views", {}).get(
                "value"
            ),
        }
        for record in response["aggregations"][
            "top_ten_artists"
        ]["buckets"]
    ]

    await redis_client.set(
        cache_key, json.dumps(artists), ex=3600
    )

    return artists


@router.get("/top/ten/songs/{country}")
@cache(expire=60)
async def get_top_ten_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
):
    try:
        response = await es_client.search(
            **top_ten_songs_query(country)
        )
    except BadRequestError as e:
        logger.error(e)

        raise HTTPException(
            status_code=400,
            detail="Invalid country",
        )

    songs = []
    for record in response["hits"]["hits"]:
        song = {
            "title": record["_source"]["title"],
            "artist": record["_source"]["artist"],
            "album": record["_source"]["album"][
                "title"
            ],
            "views": record["_source"]
            .get("views_per_country", {})
            .get(country),
        }
        songs.append(song)

    return songs
