import openai
import os
from dotenv import load_dotenv
from main import query
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
    ]
    yield {"messages": messages}


app = FastAPI(
    title="🤖 Chatbot App", lifespan=lifespan
)


API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
MODEL_ENGINE = "gpt-3.5-turbo"


@app.post("/message")
async def prompt_message(
    request: Request, prompt: str
):
    request.state.messages.append(
        {"role": "user", "content": prompt}
    )
    response = query(prompt)
    request.state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    return response


@app.get("/messages")
async def get_messages(request: Request):
    return request.state.messages
