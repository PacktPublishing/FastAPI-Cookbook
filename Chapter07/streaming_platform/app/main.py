from asyncio import gather
from contextlib import asynccontextmanager

from bson import ObjectId
from fastapi import (
    Body,
    Depends,
    FastAPI,
    HTTPException,
)
from fastapi.encoders import ENCODERS_BY_TYPE

from app import main_search
from app.database import mongo_database
from app.db_connection import (
    ping_elasticsearch_server,
    ping_mongo_db_server,
)

ENCODERS_BY_TYPE[ObjectId] = str


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

    return {
        "message": "Song added successfully",
        "id": str(song["_id"]),
    }


@app.get("/song/{song_id}")
async def get_song(
    song_id: str,
    db=Depends(mongo_database),
):
    song = await db.songs.find_one(
        {"_id": ObjectId(song_id)}
    )
    if not song:
        raise HTTPException(
            status_code=404, detail="Song not found"
        )
    return song


@app.get("/songs")
async def get_songs(
    db=Depends(mongo_database),
):
    songs = await db.songs.find().to_list(None)
    return songs


@app.put("/song/{song_id}")
async def update_song(
    song_id: str,
    updated_song: dict,
    db=Depends(mongo_database),
):
    result = await db.songs.update_one(
        {"_id": ObjectId(song_id)},
        {"$set": updated_song},
    )
    if result.modified_count == 1:
        return {"message": "Song updated successfully"}

    raise HTTPException(
        status_code=404, detail="Song not found"
    )


@app.delete("/song/{song_id}")
async def delete_song(
    song_id: str,
    db=Depends(mongo_database),
):
    result = await db.songs.delete_one(
        {"_id": ObjectId(song_id)}
    )
    if result.deleted_count == 1:
        return {"message": "Song deleted successfully"}

    raise HTTPException(
        status_code=404, detail="Song not found"
    )
