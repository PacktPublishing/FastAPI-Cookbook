from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/chatroom")
async def chatroom(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    await websocket.close()
