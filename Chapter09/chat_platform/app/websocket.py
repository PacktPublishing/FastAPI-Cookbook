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
        self, message: str, websocket: WebSocket
    ):
        await websocket.send_text(message)

    async def broadcast(
        self, message: str, exclude: WebSocket = None
    ):
        for connection in (
            self.active_connections
        ):  # TODO better refactor
            if connection == exclude:
                continue
            await connection.send_text(message)
