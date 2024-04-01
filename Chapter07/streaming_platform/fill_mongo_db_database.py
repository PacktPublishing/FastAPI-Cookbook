import asyncio
import logging

from app.db_connection import (
    mongo_client,
    ping_mongo_db_server,
)
from songs_info import songs_info

db = mongo_client.beat_streaming
collection = db["songs"]


async def insert_songs():
    # Generate JSON files
    for i, song_info in enumerate(songs_info, start=1):
        # Connect to MongoDB

        # Insert song info into MongoDB
        await collection.insert_one(song_info)
        logging.info(f"{song_info['title']} inserted")

        # Close the MongoDB connection


async def main():
    await ping_mongo_db_server()
    await insert_songs()


if __name__ == "__main__":
    asyncio.run(main())
