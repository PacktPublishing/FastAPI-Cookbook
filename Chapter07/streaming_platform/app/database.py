from app.db_connection import es_client, mongo_client

database = mongo_client.beat_streaming


def mongo_database():
    return database


songs_index_mapping = {
    "mappings": {
        "properties": {
            "artist": {"type": "keyword"},
            "views_per_country": {
                "type": "object",
                "dynamic": True,
            },
        }
    }
}


async def create_es_index():
    await es_client.options(
        ignore_status=[400, 404]
    ).indices.create(
        index="songs_index",
        body=songs_index_mapping,
    )
