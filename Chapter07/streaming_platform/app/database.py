from app.db_connection import client

database = client.beat_streaming

songs = database.songs