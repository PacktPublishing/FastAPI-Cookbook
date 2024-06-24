from contextlib import asynccontextmanager
from typing import Annotated, Tuple

from cohere import ChatMessage
from fastapi import Body, FastAPI, Request
from pydantic import BaseModel

from handlers import generate_chat_completion


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"messages": []}


app = FastAPI(
    title="Chef Cuisine Chatbot App",
    lifespan=lifespan,
)


@app.post("/query")
async def query_chat_bot(
    request: Request,
    query: Annotated[str, Body(min_length=1)],
) -> str:
    answer = await generate_chat_completion(
        query, request.state.messages
    )
    return answer


class MessagesResponse(BaseModel):
    messages: list[Tuple[str, str]]

    @classmethod
    def from_chat_messages(
        cls, messages: list[ChatMessage]
    ):
        return cls(
            messages=[
                (message.role, message.message)
                for message in messages
            ]
        )


@app.get("/messages")
def get_conversation_history(
    request: Request,
) -> MessagesResponse:
    return MessagesResponse.from_chat_messages(
        messages=request.state.messages
    )


@app.post("/restart-conversation")
def restart_conversation(request: Request):
    request.state.messages = []
    return {"message": "Conversation restarted"}
