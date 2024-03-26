from app.db_connection import es_client
from songs_info import songs_info

mapping = {
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


async def fill_elastichsearch():
    await es_client.options(
        ignore_status=[400, 404]
    ).indices.create(
        index="songs_index",
        body=mapping,
    )

    for song in songs_info:
        await es_client.index(
            index="songs_index", body=song
        )
    await es_client.close()


async def delete_all_indexes():
    await es_client.options(
        ignore_status=[400, 404]
    ).indices.delete(index="*")
    await es_client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(fill_elastichsearch())
