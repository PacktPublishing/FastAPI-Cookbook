import logging

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.websockets import WebSocketDisconnect

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.websocket("/chatroom")
async def chatroom(websocket: WebSocket):
    if not websocket.headers.get("authorization"):
        return await websocket.close()

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
                return await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE,
                    reason="Disconnecting...",
                )
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason=(
                        "You are not allowed "
                        "to send this message"
                    ),
                )
    except WebSocketDisconnect:
        logger.warn("Connection closed by the client")
