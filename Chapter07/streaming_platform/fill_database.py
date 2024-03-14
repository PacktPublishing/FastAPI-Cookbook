import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.db_connection import ping_server

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(message)s",
)

# Define a list of song information

songs_info = [
    {
        "title": "Song 1",
        "artist": "Artist 1",
        "album": "Album A",
        "release_year": 2001,
    },
    {
        "title": "Song 2",
        "artist": "Artist 2",
        "album": "Album B",
        "release_year": 2002,
    },
    {
        "title": "Song 3",
        "artist": "Artist 3",
        "album": "Album C",
        "release_year": 2003,
    },
    {
        "title": "Song 4",
        "artist": "Artist 4",
        "album": "Album D",
        "release_year": 2004,
    },
    {
        "title": "Song 5",
        "artist": "Artist 5",
        "album": "Album E",
        "release_year": 2005,
    },
    {
        "title": "Song 6",
        "artist": "Artist 6",
        "album": "Album F",
        "release_year": 2006,
    },
    {
        "title": "Song 7",
        "artist": "Artist 7",
        "album": "Album G",
        "release_year": 2007,
    },
    {
        "title": "Song 8",
        "artist": "Artist 8",
        "album": "Album H",
        "release_year": 2008,
    },
    {
        "title": "Song 9",
        "artist": "Artist 9",
        "album": "Album I",
        "release_year": 2009,
    },
    {
        "title": "Song 10",
        "artist": "Artist 10",
        "album": "Album J",
        "release_year": 2010,
    },
    {
        "title": "Song 11",
        "artist": "Artist 11",
        "album": "Album K",
        "release_year": 2011,
    },
    {
        "title": "Song 12",
        "artist": "Artist 12",
        "album": "Album L",
        "release_year": 2012,
    },
    {
        "title": "Song 13",
        "artist": "Artist 13",
        "album": "Album M",
        "release_year": 2013,
    },
]


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.beat_streaming
collection = db["songs"]


async def insert_songs():
    # Generate JSON files
    for i, song_info in enumerate(songs_info, start=1):
        # Connect to MongoDB

        # Insert song info into MongoDB
        await collection.insert_one(song_info)
        logging.info(f"{song_info['title']} inserted")

        # Close the MongoDB connection


asyncio.run(ping_server())
asyncio.run(insert_songs())
