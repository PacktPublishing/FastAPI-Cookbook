import asyncio
import logging
from operator import ge
from platform import release

from motor.motor_asyncio import AsyncIOMotorClient

from app.db_connection import ping_mongo_db_server

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(message)s",
)

# Define a list of song information

songs_info = [
    {
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "album": "÷ (Divide)",
        "release_year": 2017,
        "genre": "Pop",
        "views_per_country": {
            "US": 50_000_000,
            "UK": 30_000_000,
            "France": 20_000_000,
            "Italy": 10_000_000,
        },
    },
    {
        "title": "Despacito",
        "artist": "Luis Fonsi ft. Daddy Yankee",
        "album": "Despacito & Mis Grandes Éxitos",
        "release_year": 2017,
        "genre": "latin pop",
        "views_per_country": {
            "India": 50_000_000,
            "UK": 35_000_150_000,
            "Mexico": 60_000_000,
            "Spain": 40_000_000,
        },
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "release_year": 2020,
        "genre": "R&B",
        "views_per_country": {
            "US": 20_000_000,
            "UK": 15_000_000,
            "France": 10_000_000,
            "Italy": 5_000_000,
        },
    },
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "album": "A Night at the Opera",
        "release_year": 1975,
        "genre": "classic rock",
    },
    {
        "title": "Hips Don't Lie",
        "artist": "Shakira ft. Wyclef Jean",
        "album": "Oral Fixation, Vol. 2",
        "release_year": 2006,
        "genre": "Latin Pop",
        "views_per_country": {
            "US": 10_030_000,
            "UK": 15_000_000,
            "France": 10_000_000,
            "Germany": 5_000_000,
            "Italy": 5_000_000,
        },
    },
    {
        "title": "Dance Monkey",
        "artist": "Tones and I",
        "album": "The Kids Are Coming",
        "release_year": 2019,
        "genre": "Pop",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "France": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "Old Town Road",
        "artist": "Lil Nas X ft. Billy Ray Cyrus",
        "album": "7",
        "release_year": 2019,
        "genre": "country Rap",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "France": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "Someone You Loved",
        "artist": "Lewis Capaldi",
        "album": "Divinely Uninspired to a Hellish Extent",
        "release_year": 2019,
        "genre": "Pop",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "France": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "Uptown Funk",
        "artist": "Mark Ronson ft. Bruno Mars",
        "album": "Uptown Special",
        "release_year": 2014,
        "genre": "Funk/pop",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "France": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "Cheap Thrills",
        "artist": "Sia ft. Sean Paul",
        "album": "This Is Acting",
        "release_year": 2016,
        "genre": "Pop",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "France": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "7 Rings",
        "artist": "Ariana Grande",
        "album": "Thank U, Next",
        "release_year": 2019,
        "genre": "Pop",
        "views_per_country": {
            "US": 30_000_000,
            "UK": 20_000_000,
            "Germany": 15_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "SICKO MODE",
        "artist": "Travis Scott",
        "album": "Astroworld",
        "release_year": 2018,
        "genre": "Hip-Hop",
    },
    {
        "title": "God's Plan",
        "artist": "Drake",
        "album": "Scorpion",
        "release_year": 2018,
        "genre": "Hip-Hop",
    },
    {
        "title": "WAP",
        "artist": "Cardi B ft. Megan Thee Stallion",
        "album": "WAP (feat. Megan Thee Stallion)",
        "release_year": 2020,
        "genre": "Hip-Hop",
    },
    {
        "title": "Gangnam Style",
        "artist": "PSY",
        "album": "PSY 6 (Six Rules), Part 1",
        "release_year": 2012,
        "genre": "K-Pop",
    },
    {
        "title": "Rolling in the Deep",
        "artist": "Adele",
        "album": "21",
        "release_year": 2011,
        "genre": "Pop",
    },
    {
        "title": "Radioactive",
        "artist": "Imagine Dragons",
        "album": "Night Visions",
        "release_year": 2012,
        "genre": "alternative Rock",
    },
    {
        "title": "Can't Stop the Feeling!",
        "artist": "Justin Timberlake",
        "album": "Trolls: Original Motion Picture Soundtrack",
        "release_year": 2016,
        "genre": "Pop",
    },
    {
        "title": "Rockstar",
        "artist": "Post Malone ft. 21 Savage",
        "album": "Beerbongs & Bentleys",
        "release_year": 2018,
        "genre": "Hip-Hop",
    },
    {
        "title": "Hello",
        "artist": "Adele",
        "album": "25",
        "release_year": 2015,
        "genre": "Pop",
    },
    {
        "title": "Thunder",
        "artist": "Imagine Dragons",
        "album": "Evolve",
        "release_year": 2017,
        "genre": "Alternative Rock",
    },
    {
        "title": "Hotline Bling",
        "artist": "Drake",
        "album": "Views",
        "release_year": 2016,
        "genre": "Hip-Hop",
    },
    {
        "title": "Closer",
        "artist": "The Chainsmokers ft. Halsey",
        "album": "Collage",
        "release_year": 2016,
        "genre": "EDM/Pop",
    },
    {
        "title": "Love Yourself",
        "artist": "Justin Bieber",
        "album": "Purpose",
        "release_year": 2015,
        "genre": "Pop",
    },
    {
        "title": "The Hills",
        "artist": "The Weeknd",
        "album": "Beauty Behind the Madness",
        "release_year": 2015,
        "genre": "R&B",
    },
    {
        "title": "Sucker",
        "artist": "Jonas Brothers",
        "album": "Happiness Begins",
        "release_year": 2019,
        "genre": "Pop",
    },
    {
        "title": "Sorry",
        "artist": "Justin Bieber",
        "album": "Purpose",
        "release_year": 2015,
        "genre": "Pop",
    },
    {
        "title": "Stressed Out",
        "artist": "Twenty One Pilots",
        "album": "Blurryface",
        "release_year": 2015,
        "genre": "Alternative/Indie",
    },
    {
        "title": "Djadja",
        "artist": "Aya Nakamura",
        "album": "Nakamura",
        "release_year": 2018,
        "genre": "Afrobeat/R&B",
        "views_per_country": {
            "US": 40_000_000,
            "UK": 10_000_000,
            "France": 150_000_000,
            "Italy": 10_000_000,
            "Australia": 50_000_000,
        },
    },
    {
        "title": "Virtual Insanity",
        "artist": "Jamiroquai",
        "album": "Travelling Without Moving",
        "release_year": 1996,
        "genre": "Funk/Disco",
        "views_per_country": {
            "US": 40_000_000,
            "UK": 40_010_040,
            "France": 10_000_000,
        },
    },
    {
        "title": "Formidable",
        "artist": "Stromae",
        "album": "Racine Carrée",
        "release_year": 2013,
        "gerne": "Hip-Hop/World",
        "views_per_country": {
            "France": 50_000_000,
            "Belgium": 20_000_000,
            "Germany": 10_000_000,
            "Suiss": 5_000_000,
        },
    },
    {
        "title": "Me Staje Appennenn' Amò",
        "artist": "Liberato",
        "album": "Liberato",
        "release_year": 2019,
        "genre": "Alternative R&B",
        "views_per_country": {
            "Italy": 60_467_002,
            "UK": 20_000_000,
            "France": 10_000_000,
            "Germany": 5_000_000,
        },
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


if __name__ == "__main__":
    asyncio.run(ping_mongo_db_server())
    asyncio.run(insert_songs())
