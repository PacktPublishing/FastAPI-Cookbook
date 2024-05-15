from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Body, FastAPI, Request

from documents import load_documents
from model import query_assistant


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"documents": load_documents()}


app = FastAPI(title="Chatbot App", lifespan=lifespan)


@app.post("/message")
async def prompt_message(
    request: Request,
    prompt: Annotated[str, Body()],
) -> str:
    documents = request.state.documents
    response = await query_assistant(
        prompt, documents
    )
    return response
