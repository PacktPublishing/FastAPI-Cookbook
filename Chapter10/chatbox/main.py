from typing import Annotated, Tuple

from fastapi import Body, FastAPI

from handlers import (
    generate_chat_completion,
    messages,
)

app = FastAPI(title="Chef Cuisine Chatbot App")


@app.post("/query")
async def query_chat_box(
    query: Annotated[str, Body()],
) -> str:
    completion = await generate_chat_completion(query)
    return completion


@app.get("/messages")
def get_conversation_messages()-> list[Tuple[str, str]]:
    formatted_messages = []
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            continue
        role = (
            "Chef Cuisine"
            if message["role"] == "assistant"
            else "You"
        )
        formatted_messages.append(
            f"{role}: {message['content']}"
        )
    return formatted_messages

