from asyncio import gather
from contextlib import asynccontextmanager

from fastapi import Body, Depends, FastAPI

from app import main_search
from app.database import database
from app.db_connection import (
    ping_elasticsearch_server,
    ping_mongo_db_server,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await gather(
        ping_mongo_db_server(),
        ping_elasticsearch_server(),
    )
    yield


app = FastAPI(lifespan=lifespan)

try:
    app.include_router(main_search.router)
except Exception:
    pass


def mongo_database():
    return database


@app.post("/song")
async def add_song(
    song: dict = Body(
        example={
            "title": "My Song",
            "artist": "My Artist",
            "genre": "My Genre",
        },
    ),
    mongo_db=Depends(mongo_database),
    es_client=Depends(
        main_search.get_elasticsearch_client
    ),
):
    await es_client.index(
        index="songs_index", body=song
    )
    await mongo_db.songs.insert_one(song)

    return {"message": "Song added successfully"}


@app.get("/song/{song_id}")
async def get_song(
    song_id: str,
    db=Depends(mongo_database),
):
    song = await db.songs.find_one({"_id": song_id})
    if song:
        return song
    else:
        return {"message": "Song not found"}


@app.get("/songs")
async def get_songs(
    db=Depends(mongo_database),
):
    songs = []
    async for song in db.songs.find():
        songs.append(song)
    return songs


@app.put("/song/{song_id}")
async def update_song(
    song_id: str,
    updated_song: dict,
    db=Depends(mongo_database),
):
    result = await db.songs.update_one(
        {"_id": song_id}, {"$set": updated_song}
    )
    if result.modified_count == 1:
        return {"message": "Song updated successfully"}
    else:
        return {"message": "Song not found"}


@app.delete("/song/{song_id}")
async def delete_song(
    song_id: str,
    db=Depends(mongo_database),
):
    result = await db.songs.delete_one({"_id": song_id})
    if result.deleted_count == 1:
        return {"message": "Song deleted successfully"}
    else:
        return {"message": "Song not found"}
