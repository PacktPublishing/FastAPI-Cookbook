from app.db_connection import mongo_client

database = mongo_client.beat_streaming

songs = database.songs
