from cohere import AsyncClient, ChatMessage
from cohere.core.api_error import ApiError
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SYSTEM_MESSAGE = (
    "You are a skilled Italian top chef "
    "expert in Italian cuisine tradition "
    "that suggest the best recipes unveiling "
    "tricks and tips from Grandma's Kitchen"
    "shortly and concisely."
)


client = AsyncClient()


async def generate_chat_completion(
    user_query=" ", messages=[]
) -> str:
    try:
        response = await client.chat(
            message=user_query,
            model="command-r-plus",
            preamble=SYSTEM_MESSAGE,
            chat_history=messages,
        )
        messages.extend(
            [
                ChatMessage(
                    role="USER", message=user_query
                ),
                ChatMessage(
                    role="CHATBOT",
                    message=response.text,
                ),
            ]
        )
        return response.text

    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code, detail=e.body
        )
