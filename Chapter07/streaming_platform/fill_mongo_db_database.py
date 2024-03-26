import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.db_connection import ping_mongo_db_server
from songs_info import songs_info

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(message)s",
)

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


if __name__ == "__main__":
    asyncio.run(ping_mongo_db_server())
    asyncio.run(insert_songs())
