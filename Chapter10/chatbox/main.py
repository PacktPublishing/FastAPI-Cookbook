from typing import Annotated
from fastapi import FastAPI, Body
from handlers import generate_chat_completion

# Streamlit App
app = FastAPI(title="😂 Funny Chatbot App")


@app.post("/query")
async def query_chat_box(
    query: Annotated[str, Body()],
):
    completion = generate_chat_completion(query)
    return completion
