from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.database import database
from app.db_connection import ping_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_server()
    yield


app = FastAPI(lifespan=lifespan)


def database_dependency():
    return database


@app.post("/song")
async def add_song(
    song: dict,
    db=Depends(database_dependency),
):
    await db.songs.insert_one(song)
    return {"message": "Song added successfully"}


@app.get("/song/{song_id}")
async def get_song(
    song_id: str,
    db=Depends(database_dependency),
):
    song = await db.songs.find_one({"_id": song_id})
    if song:
        return song
    else:
        return {"message": "Song not found"}


@app.get("/songs")
async def get_songs(
    db=Depends(database_dependency),
):
    songs = []
    async for song in db.songs.find():
        songs.append(song)
    return songs


@app.put("/song/{song_id}")
async def update_song(
    song_id: str,
    updated_song: dict,
    db=Depends(database_dependency),
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
    db=Depends(database_dependency),
):
    result = await db.songs.delete_one({"_id": song_id})
    if result.deleted_count == 1:
        return {"message": "Song deleted successfully"}
    else:
        return {"message": "Song not found"}
