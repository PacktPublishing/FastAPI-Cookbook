from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Request
from documents import load_documents
from contextlib import asynccontextmanager
from model import query_assistant

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"documents": load_documents()}


app = FastAPI(title="Chatbot App", lifespan=lifespan)


@app.post("/message")
async def prompt_message(
    request: Request,
    prompt: Annotated[str, Body()],
):
    documents = request.state.documents
    response = await query_assistant(
        prompt, documents
    )
    return response
