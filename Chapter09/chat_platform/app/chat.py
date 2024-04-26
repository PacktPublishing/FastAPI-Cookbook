from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse

from app.templating import templates
from app.ws_manager import ConnectionManager

conn_manager = ConnectionManager()


router = APIRouter()


@router.websocket("/chatroom/{username}")
async def chatroom_endpoint(
    websocket: WebSocket, username: str
):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast(
        {
            "sender": "system",
            "message": f"{username} joined the chat",
        },
        exclude=websocket,
    )

    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast(
                {"sender": username, "message": data},
                exclude=websocket,
            )
            await conn_manager.send_personal_message(
                {"sender": "You", "message": data},
                websocket,
            )
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast(
            {
                "sender": "system",
                "message": f"Client #{username} "
                "left the chat",
            }
        )


@router.get("/chatroom/{username}")
async def chatroom_page_endpoint(
    request: Request, username: str
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="chatroom.html",
        context={"username": username},
    )
