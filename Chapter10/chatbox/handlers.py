from dotenv import load_dotenv
from openai import AsyncClient

load_dotenv()

SYSTEM_MESSAGE = (
    "You are a skilled Italian top chef "
    "expert in Italian cuisine tradition "
    "that suggest the best recipes unveiling "
    "tricks and tips from Grandma's Kitchen"
    "shortly and concisely."
)

messages = [
    {"role": "system", "content": SYSTEM_MESSAGE}
]

client = AsyncClient()


def to_dict(obj):
    return {
        "content": obj.content,
        "role": obj.role,
    }


async def generate_chat_completion(user_input=""):
    messages.append(
        {"role": "user", "content": user_input}
    )
    completion = (
        await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    )
    message = completion.choices[0].message
    messages.append(to_dict(message))
    return message.content
