from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.security import (
    fake_token_resolver,
    get_username_from_token,
)
from app.ws_manager import ConnectionManager

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/exclusive-chatroom")
async def exclusive_chatroom(
    request: Request,
):
    token = request.cookies.get("chatroomtoken")
    user = fake_token_resolver(token)
    if not user:
        return RedirectResponse(
            url="/login?redirecturl=http://localhost:8000/exclusive-chatroom",
        )
    return templates.TemplateResponse(
        request=request,
        name="chatroom.html",
        context={"username": user.username},
    )


connection_manager = ConnectionManager()


@router.websocket("/ws-eclusive")
async def websocket_chatroom(
    websocket: WebSocket,
    username: Annotated[
        get_username_from_token, Depends()
    ],
):
    await connection_manager.connect(websocket)
    await connection_manager.broadcast(
        {
            "sender": "system",
            "message": f"{username} joined the chat",
        },
        exclude=websocket,
    )
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(
                {
                    "sender": username,
                    "message": data,
                },
                exclude=websocket,
            )
            await connection_manager.send_personal_message(
                {"sender": "You", "message": data},
                websocket,
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(
            f"Client #{username} left the chat"
        )
