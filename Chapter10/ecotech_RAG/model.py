from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_openai import (
    ChatOpenAI,
)

from prompting import (
    chat_prompt_template,
)

load_dotenv()


model = ChatOpenAI(
    model="gpt-3.5-turbo", temperature=0.3
)

chain = (
    chat_prompt_template | model | StrOutputParser()
)
