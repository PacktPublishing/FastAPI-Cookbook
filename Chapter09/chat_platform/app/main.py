import logging

from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect

from app.websocket import ConnectionManager

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.websocket(
    "/chatroom"
)  # TODO change name of the function and endpoint
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
                    reason="Inappropriate message",
                )
    except WebSocketDisconnect:
        logger.warn("Connection closed by the client")


templates = Jinja2Templates(directory="templates")


@app.get("/room/{username}")
async def chatroom_endpoint(
    request: Request, username: str
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="chatroom.html",
        context={"username": username},
    )


connection_manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_chatroom(
    websocket: WebSocket, username: str
):
    await connection_manager.connect(websocket)
    await connection_manager.broadcast(
        f"Client #{username} joined the chat", exclude=websocket
    )
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(
                f"You wrote: {data}", websocket
            )
            await connection_manager.broadcast(
                f"Client #{username} says: {data}", exclude=websocket
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(
            f"Client #{username} left the chat"
        )
