import logging

from fastapi import (
    FastAPI,
    WebSocket,
)
from fastapi.websockets import WebSocketDisconnect

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.websocket("/chatroom")
async def chatroom(websocket: WebSocket):
    if not websocket.headers.get("Authorization"):
        return
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            if data == "disconnect":
                logger.warn("Disconnecting...")
                await websocket.close()
                break

    except WebSocketDisconnect:
        logger.warn("Connection closed")
