from fastapi import APIRouter, Depends

from app.db_connection import es_client

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


def get_elasticsearch_client():
    return es_client


@router.get("/top/ten/songs/{country}")
async def get_top_ten_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
):
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
    response = await es_client.search(
        index="songs_index",
        query=query,
        size=10,
        sort=sort,
        source=source,
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


@router.get("/top/ten/artists/{country}")
async def top_ten_artist_by_country(
    country: str,
    es_client=Depends(get_elasticsearch_client),
):
    views_field = f"views_per_country.{country}"
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
        index="songs_index", size=0, aggs=aggs
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
