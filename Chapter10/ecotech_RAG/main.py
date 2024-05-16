from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Body, FastAPI, Request

from documents import get_context, load_documents
from model import chain


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"documents": load_documents()}


app = FastAPI(
    title="Ecotech AI Assistant", lifespan=lifespan
)


@app.post("/message")
async def prompt_message(
    request: Request,
    prompt: Annotated[str, Body()],
) -> str:
    documents = request.state.documents
    response = await chain.ainvoke(
        {
            "question": prompt,
            "context": get_context(
                prompt, documents
            ),
        }
    )
    return response
