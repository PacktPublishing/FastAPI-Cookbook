import json
import logging

from elasticsearch import BadRequestError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from app.db_connection import es_client, redis_client

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


def get_elasticsearch_client():
    return es_client


def get_redis_client():
    return redis_client


@router.get("/top/ten/songs/{country}")
async def get_top_ten_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
    redis_client=Depends(get_redis_client),
):
    cache_key = f"top_ten_songs_{country}"

    cached_data = await redis_client.get(cache_key)
    if cached_data:
        logger.info(
            f"Returning cached data for {country}"
        )
        return json.loads(cached_data)

    views_field = f"views_per_country.{country}"
    query = {
        "bool": {
            "must": {"match_all": {}},
            "filter": [
                {"exists": {"field": views_field}}
            ],
        }
    }
    sort = {views_field: {"order": "desc"}}
    source = [
        "title",
        views_field,
        "album.title",
        "artist",
    ]
    try:
        response = await es_client.search(
            index="songs_index",
            query=query,
            size=10,
            sort=sort,
            source=source,
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

    await redis_client.set(
        cache_key, json.dumps(songs), ex=60
    )

    return songs


@router.get("/top/ten/artists/{country}")
@cache(expire=60)
async def top_ten_artist_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
):
    logger.info(
        f"Getting top ten artists for {country}"
    )
    views_field = f"views_per_country.{country}"

    query = {
        "bool": {
            "filter": [
                {"exists": {"field": views_field}}
            ],
        }
    }

    aggs = {
        "top_ten_artists": {
            "terms": {
                "field": "artist",
                "size": 10,
                "order": {"views": "desc"},
            },
            "aggs": {
                "views": {
                    "sum": {
                        "field": views_field,
                        "missing": 0,
                    }
                }
            },
        }
    }

    response = await es_client.search(
        index="songs_index",
        size=0,
        query=query,
        aggs=aggs,
    )
    return [
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
