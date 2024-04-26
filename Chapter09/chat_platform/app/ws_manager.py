import asyncio

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self, message: dict, websocket: WebSocket
    ):
        await websocket.send_json(message)

    async def broadcast(
        self, message: dict, exclude: WebSocket = None
    ):
        tasks = [
            connection.send_json(message)
            for connection in self.active_connections
            if connection != exclude
        ]
        await asyncio.gather(*tasks)
