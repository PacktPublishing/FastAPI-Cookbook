from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_cohere import ChatCohere

from prompting import (
    chat_prompt_template,
)

load_dotenv()

model = ChatCohere(model="command-r-plus")

chain = (
    chat_prompt_template | model | StrOutputParser()
)
