from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_core.document_loaders.base import (
    Document,
)
from langchain_openai import (
    ChatOpenAI,
)

from documents import load_embeddings
from prompting import (
    chat_prompt_template,
)

load_dotenv()


model = ChatOpenAI(
    model="gpt-3.5-turbo", temperature=0.3
)


async def query_assistant(
    user_query: str, documents: list[Document]
) -> str:
    retriever = load_embeddings(
        user_query, documents
    )

    chain = (
        chat_prompt_template
        | model
        | StrOutputParser()
    )

    response = await chain.ainvoke(
        {
            "question": user_query,
            "context": retriever,
        }
    )
    return response
