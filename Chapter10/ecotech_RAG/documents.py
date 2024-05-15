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
    raw_documents = TextLoader(
        "./docs/faq_ecotech.txt"
    ).load()
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )
    return text_splitter.split_documents(
        raw_documents
    )


def load_embeddings(
    user_query: str, documents: list[Document]
) -> str:
    db = Chroma.from_documents(
        documents, OpenAIEmbeddings()
    )
    docs = db.similarity_search(user_query)
    print(docs)
    context = docs[0].page_content
    return context
