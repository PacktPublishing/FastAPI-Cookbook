from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain_community.document_loaders import (
    TextLoader,
)
from langchain_core.documents.base import Document


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
