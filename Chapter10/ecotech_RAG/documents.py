from pathlib import Path
from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain_community.document_loaders import (
    TextLoader,
)
from langchain_community.vectorstores import Chroma
from langchain_core.document_loaders.base import (
    Document,
)
from langchain_openai import OpenAIEmbeddings


def load_documents() -> list[Document]:
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )

    raw_documents = (
        TextLoader(filepath).load()
        for filepath in Path().glob("./docs/*.txt")
    )

    return text_splitter.split_documents(
        raw_documents
    )


def get_context(
    user_query: str, documents: list[Document]
) -> str:
    db = Chroma.from_documents(  # move this to load_docouments function
        documents, OpenAIEmbeddings()
    )
    docs = db.similarity_search(user_query)
    context = docs[0].page_content
    return context
